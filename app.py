import base64
import json
import logging
import os
from flask import Flask, redirect, request, render_template, make_response

app = Flask(__name__)

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

def fix_padding(encoded_str):
    """Ensures proper base64 padding for decoding."""
    missing_padding = len(encoded_str) % 4
    if missing_padding:
        encoded_str += '=' * (4 - missing_padding)
    return encoded_str

def decode_jwt(token):
    """ Decodes a JWT (JSON Web Token) while handling padding issues. """
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {"error": "Invalid JWT format (must have 3 parts: header.payload.signature)"}

        # Fix padding and decode header & payload
        header = json.loads(base64.urlsafe_b64decode(fix_padding(parts[0])).decode())
        payload = json.loads(base64.urlsafe_b64decode(fix_padding(parts[1])).decode())

        return {"header": header, "payload": payload}
    except Exception as e:
        logging.error(f"Error decoding JWT: {e}")
        return {"error": str(e)}

@app.route('/jupyter')
def jupyter():
    headers = {key: value for key, value in request.headers.items()}
    query_params = request.args.to_dict()
    cookies = request.cookies.to_dict()

    # Extract the JWT from the X-Auth-Id-Token header
    jwt_token = headers.get("X-Auth-Id-Token", None)
    decoded_token = decode_jwt(jwt_token) if jwt_token else {"error": "No X-Auth-Id-Token found in headers"}

    # Debugging logs
    logging.debug(f"Received Headers: {headers}")
    logging.debug(f"JWT Token: {jwt_token}")
    logging.debug(f"Decoded JWT: {decoded_token}")

    return render_template("jupyter.html", headers=headers, query_params=query_params, cookies=cookies, decoded_token=decoded_token)

@app.route('/jupyter/logout')
def logout():
    """Delete authentication cookies and then redirect to Keycloak logout page."""
    
    # Create an empty response (no redirect yet)
    response = make_response()

    # DELETE cookies by setting `expires=0` and `max_age=0`
    cookies_to_delete = [
        "_oauth2_proxy_0",
        "_oauth2_proxy_1",
        "AUTH_SESSION_ID",
        "KC_AUTH_SESSION_HASH",
        "KC_RESTART"
    ]
    
    for cookie in cookies_to_delete:
        response.delete_cookie(cookie, path="/jupyter/logout", domain=MY_DOMAIN)

    # # Now redirect AFTER deleting cookies
    # response = make_response(redirect(OIDC_LOGOUT_URL))  
    return response

@app.route('/')
def hello_world():
    return "Hello World from your EKS Cluster!"

# Get values from environment variables, with defaults
port = int(os.getenv("FLASK_PORT", 8000))
debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"

#OIDC_LOGOUT_URL for keycloak https://{keycloak server}/realms/isambard/protocol/openid-connect/logout
OIDC_LOGOUT_URL = os.getenv("OIDC_URL", "") 
MY_DOMAIN = os.getenv("DOMAIN", "")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=debug)
