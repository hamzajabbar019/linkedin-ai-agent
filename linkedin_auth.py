import os
import secrets
import urllib.parse
import requests

from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "openid profile w_member_social"
if not CLIENT_ID:
    raise ValueError("LINKEDIN_CLIENT_ID is not set in .env")

if not CLIENT_SECRET:
    raise ValueError("LINKEDIN_CLIENT_SECRET is not set in .env")


app = Flask(__name__)

STATE = secrets.token_urlsafe(32)


@app.route("/")
def login():

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": STATE,
        "scope": SCOPES,
    }

    authorization_url = (
        "https://www.linkedin.com/oauth/v2/authorization?"
        + urllib.parse.urlencode(params)
    )

    return f"""
    <h2>LinkedIn AI Agent</h2>

    <p>
        <a href="{authorization_url}">
            Login with LinkedIn
        </a>
    </p>
    """


@app.route("/callback")
def callback():

    code = request.args.get("code")
    returned_state = request.args.get("state")
    error = request.args.get("error")

    # --------------------------------------------------
    # Check for LinkedIn authorization error
    # --------------------------------------------------

    if error:
        return f"""
        <h2>LinkedIn authorization failed</h2>
        <p>{error}</p>
        """

    # --------------------------------------------------
    # Check OAuth state
    # --------------------------------------------------

    if returned_state != STATE:
        return """
        <h2>Security error</h2>
        <p>Invalid OAuth state.</p>
        """

    # --------------------------------------------------
    # Check authorization code
    # --------------------------------------------------

    if not code:
        return """
        <h2>Error</h2>
        <p>No authorization code received.</p>
        """

    # --------------------------------------------------
    # Exchange authorization code for access token
    # --------------------------------------------------

    token_response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",

        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },

        timeout=30,
    )

    # --------------------------------------------------
    # Check token response
    # --------------------------------------------------

    if token_response.status_code != 200:

        return f"""
        <h2>Token request failed</h2>

        <pre>{token_response.text}</pre>
        """

    token_data = token_response.json()

    access_token = token_data.get("access_token")
    expires_in = token_data.get("expires_in")

    # --------------------------------------------------
    # Make sure token exists
    # --------------------------------------------------

    if not access_token:

        return """
        <h2>Error</h2>
        <p>No access token was returned.</p>
        """

    # --------------------------------------------------
    # Save token locally
    # --------------------------------------------------

    token_file = ".linkedin_token"

    try:

        with open(
            token_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(access_token)

    except Exception as save_error:

        return f"""
        <h2>Token received but could not be saved</h2>

        <pre>{save_error}</pre>
        """

    # --------------------------------------------------
    # Success
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("LINKEDIN AUTHENTICATION SUCCESSFUL")
    print("=" * 60)

    print("\nAccess token saved locally.")
    print(f"Expires in: {expires_in} seconds")
    print(f"Token file: {token_file}")

    print("\nDO NOT share this token.")
    print("=" * 60)

    return """
    <h2>LinkedIn authentication successful!</h2>

    <p>You can close this browser window.</p>

    <p>
        The access token was successfully saved
        to the local application.
    </p>
    """


if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("LINKEDIN OAUTH SERVER")
    print("=" * 60)

    print("\nOpen this URL in your browser:")
    print("http://localhost:8000")

    print("\nWaiting for LinkedIn authentication...")

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )
