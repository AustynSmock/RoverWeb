import requests

# Endpoint URLs
login_url = 'https://roverweb-86ddt01ec-austyn-smocks-projects.vercel.app//user/login'
upload_url = 'http://127.0.0.1:5000/upload'

# User credentials
login_credentials = {
    "name": "xxxxxx",
    "password": "xxxxxx"
}

file_path = 'rarar.txt'

# Start a session to persist login state
with requests.Session() as session:
    # Send login request
    login_response = session.post(login_url, json=login_credentials)

    # Check if login was successful
    if login_response.status_code == 200:
        print("Login successful.")

        # Proceed with file upload
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (file_path, file, 'text/plain')}
                response = session.post(upload_url, files=files)

                if response.status_code == 200:
                    print("File uploaded successfully.")
                else:
                    print(f"Failed to upload file. Status code: {response.status_code}")
        except FileNotFoundError:
            print(f"The file {file_path} does not exist.")
    else:
        print(f"Failed to log in. Status code: {login_response.status_code}")