import network
import socket
import time
from machine import Pin, time_pulse_us

# Wi-Fi credentials
SSID = 'ESP32-AP'
PASSWORD = '12345678'

# Login credentials
USERNAME = 'admin'
PASSWORD_AUTH = '1234'

session_authenticated = False

# Motor pins
AIN1 = Pin(25, Pin.OUT)
AIN2 = Pin(33, Pin.OUT)
BIN1 = Pin(27, Pin.OUT)
BIN2 = Pin(14, Pin.OUT)
PWMA = Pin(32, Pin.OUT)
PWMB = Pin(12, Pin.OUT)
STBY = Pin(26, Pin.OUT)

PWMA.on()
PWMB.on()
STBY.on()

# Ultrasonic sensor pins
TRIG = Pin(2, Pin.OUT)
ECHO = Pin(4, Pin.IN)

def start_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP32-AP', password='12345678',authmode=network.AUTH_WPA_WPA2_PSK) 

    while not ap.active():
        time.sleep(1)

    print("Access Point active. IP:", ap.ifconfig()[0])
    return ap.ifconfig()[0]


def move_forward():
    AIN1.on(); AIN2.off()
    BIN1.on(); BIN2.off()

def move_backward():
    AIN1.off(); AIN2.on()
    BIN1.off(); BIN2.on()

def move_left():
    AIN1.off(); AIN2.on()
    BIN1.on(); BIN2.off()

def move_right():
    AIN1.on(); AIN2.off()
    BIN1.off(); BIN2.on()

def stop():
    AIN1.off(); AIN2.off()
    BIN1.off(); BIN2.off()

def measure_distance():
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()

    try:
        pulse = time_pulse_us(ECHO, 1, 30000)
        if pulse < 0:
            return None
        dist_cm = (pulse / 2) / 29.1
        return dist_cm
    except:
        return None

def login_page():
    return """<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            background-color: #1b1b1b;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-box {
            background: #2e2e2e;
            padding: 30px;
            border-radius: 10px;
            color: white;
            box-shadow: 0 0 20px #000;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #a7e163;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <form class="login-box" method="POST" action="/login">
        <h2>Login</h2>
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Sign In</button>
    </form>
</body>
</html>"""

def html_page():
    return """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Bot Control</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #e3e9f0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 { color: #333; }
        .button-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .button {
            padding: 15px 30px;
            font-size: 16px;
            font-weight: bold;
            color: #333;
            background-color: #e3e9f0;
            border: none;
            border-radius: 15px;
            box-shadow: 9px 9px 16px #babecc, -9px -9px 16px #ffffff;
            cursor: pointer;
        }
        .button:active {
            box-shadow: inset 5px 5px 10px #babecc, inset -5px -5px 10px #ffffff;
        }
        .info {
            margin-top: 30px;
            font-size: 18px;
            color: #333;
            padding: 15px 30px;
            border-radius: 15px;
            background-color: #e3e9f0;
            box-shadow: 9px 9px 16px #babecc, -9px -9px 16px #ffffff;
        }
        a { text-decoration: none; }
    </style>
    <script>
        function updateDistance() {
            fetch('/distance')
                .then(res => res.text())
                .then(data => {
                    document.getElementById("distance").innerText = data;
                });
        }
        setInterval(updateDistance, 500);
        window.onload = updateDistance;
    </script>
</head>
<body>
    <h1>ESP32 Bot Control</h1>
    <div class="button-container">
        <a href="/forward"><button class="button">Forward</button></a>
        <a href="/left"><button class="button">Left</button></a>
        <a href="/right"><button class="button">Right</button></a>
        <a href="/backward"><button class="button">Backward</button></a>
    </div>
    <div class="info" id="distance">Loading...</div>
</body>
</html>"""

def handle_client(client):
    global session_authenticated
    request = client.recv(1024).decode('utf-8')
    print(request)

    method = request.split(' ')[0]
    path = request.split(' ')[1]

    if path.startswith('/login') and method == 'POST':
        body = request.split('\r\n\r\n')[-1]
        data = {}
        for pair in body.split('&'):
            if '=' in pair:
                key, value = pair.split('=')
                data[key] = value

        username = data.get("username", "")
        password = data.get("password", "")

        if username == USERNAME and password == PASSWORD_AUTH:
            session_authenticated = True
            client.send('HTTP/1.1 302 Found\r\nLocation: /\r\n\r\n')
        else:
            session_authenticated = False
            client.send('HTTP/1.1 401 Unauthorized\r\n\r\n<h1>Unauthorized</h1>')
        client.close()
        return

    if not session_authenticated and path != "/login":
        client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        client.send(login_page())
        client.close()
        return

    # Real-time distance AJAX call
    if path == "/distance":
        dist = measure_distance()
        if dist is None or dist > 100:
            msg = "No Obstacle Detected"
        else:
            msg = f"Obstacle Ahead: {dist:.2f} cm"
        client.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n')
        client.send(msg)
        client.close()
        return

    # Bot movement control
    if "/forward" in path:
        move_forward()
    elif "/backward" in path:
        move_backward()
    elif "/left" in path:
        move_left()
    elif "/right" in path:
        move_right()
    else:
        stop()

    # Main control UI
    client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
    client.send(html_page())
    client.close()


# Server setup
ip = start_access_point()
addr = socket.getaddrinfo(ip, 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Listening on", addr)


while True:
    try:
        client, addr = s.accept()
        handle_client(client)
    except Exception as e:
        print("Error:", e)
