import requests

TOKEN_FILE = ".linkedin_token"
LINKEDIN_VERSION = "202604"


def load_token():
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            ".linkedin_token not found. "
            "Run linkedin_auth.py first."
        )


def get_profile():
    token = load_token()

    url = "https://api.linkedin.com/v2/userinfo"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"Could not get LinkedIn profile: "
            f"{response.status_code} {response.text}"
        )

    return response.json()


def publish_post(post_text):
    """
    Publish a text post to the authenticated
    LinkedIn member account.

    Returns:
        dict with success, post_id and status_code
    """

    token = load_token()

    profile = get_profile()

    member_id = profile.get("sub")

    if not member_id:
        raise Exception(
            "LinkedIn member ID was not returned."
        )

    author = f"urn:li:person:{member_id}"

    url = "https://api.linkedin.com/rest/posts"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": LINKEDIN_VERSION,
    }

    data = {
        "author": author,
        "commentary": post_text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED"
    }

    print("\n" + "=" * 60)
    print("PUBLISHING TO LINKEDIN")
    print("=" * 60)

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=30
    )

    print(f"\nHTTP Status: {response.status_code}")

    if response.status_code in (200, 201):

        post_id = response.headers.get("x-restli-id")

        print("\n✅ LinkedIn post published successfully!")

        if post_id:
            print(f"Post ID: {post_id}")

        return {
            "success": True,
            "post_id": post_id,
            "status_code": response.status_code
        }

    print("\n❌ LinkedIn publishing failed.")
    print("Response:", response.text)

    return {
        "success": False,
        "post_id": None,
        "status_code": response.status_code,
        "error": response.text
    }


if __name__ == "__main__":

    print("\nLinkedIn API module loaded successfully.")
    print("Use publish_post(post_text) from the AI agent.")
