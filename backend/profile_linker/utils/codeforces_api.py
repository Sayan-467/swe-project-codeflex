import requests

def fetch_codeforces_profile(handle):
    """
    Fetches a Codeforces user's profile information using the official API.
    Returns their handle, current rating, max rating, rank, etc.
    """
    try:
        url = f"https://codeforces.com/api/user.info?handles={handle}"
        response = requests.get(url, timeout=10)

        # Check if API request succeeded
        if response.status_code != 200:
            print(f"Error: Codeforces API returned {response.status_code}")
            return None

        data = response.json()

        # Validate response content
        if data.get("status") != "OK" or "result" not in data:
            print("Error: Invalid data received from Codeforces API")
            return None

        user = data["result"][0]

        # Return all relevant info
        return {
            "handle": user.get("handle"),
            "rating": user.get("rating", 0),
            "max_rating": user.get("maxRating", 0),
            "rank": user.get("rank", "unrated"),
            "max_rank": user.get("maxRank", "unrated"),
            "contribution": user.get("contribution", 0),
            "friendOfCount": user.get("friendOfCount", 0),
            "organization": user.get("organization", "N/A")
        }

    except Exception as e:
        print(f"Exception while fetching Codeforces profile: {e}")
        return None
