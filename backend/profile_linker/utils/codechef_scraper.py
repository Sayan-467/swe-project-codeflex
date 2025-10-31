import requests
from bs4 import BeautifulSoup

def fetch_codechef_profile(handle):
    url = f"https://www.codechef.com/users/{handle}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Invalid CodeChef handle"}

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Extract username and full name
        name_tag = soup.find("div", class_="user-details-container").find("h1")
        name = name_tag.text.strip() if name_tag else handle

        # Rating section
        rating_section = soup.find("div", class_="rating-header")
        rating = rating_section.find("div", class_="rating-number").text.strip() if rating_section else "N/A"

        stars_tag = soup.find("span", class_="rating")
        stars = stars_tag.text.strip() if stars_tag else "N/A"

        max_rating_tag = soup.find("small")
        max_rating = max_rating_tag.text.strip().replace("(", "").replace(")", "") if max_rating_tag else "N/A"

        # Country info
        country_tag = soup.find("span", class_="user-country-name")
        country = country_tag.text.strip() if country_tag else "N/A"

        # Global and country rank
        ranks = soup.find_all("strong")
        global_rank = ranks[0].text.strip() if len(ranks) > 0 else "N/A"
        country_rank = ranks[1].text.strip() if len(ranks) > 1 else "N/A"

        # Number of problems solved
        problem_section = soup.find("section", class_="rating-data-section problems-solved")
        solved_count = 0
        if problem_section:
            all_links = problem_section.find_all("a")
            solved_count = len(all_links)

        return {
            "handle": handle,
            "name": name,
            "country": country,
            "rating": rating,
            "max_rating": max_rating,
            "stars": stars,
            "global_rank": global_rank,
            "country_rank": country_rank,
            "problems_solved": solved_count
        }

    except Exception as e:
        return {"error": f"Parsing failed: {str(e)}"}
