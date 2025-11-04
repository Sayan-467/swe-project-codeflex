import requests
from bs4 import BeautifulSoup

def fetch_discuss_explanations(problem_code: str):
    """
    Fetch meaningful CodeChef Discuss posts for a given problem.
    Filters out 'Help me' type posts and prefers 'Editorial' or 'Explanation' ones.
    """
    base_url = "https://discuss.codechef.com"
    search_url = f"{base_url}/search.json?q={problem_code}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()

        topics = data.get("topics", [])
        posts = []

        for topic in topics:
            title = topic.get("title", "").lower()
            if any(bad in title for bad in ["help", "doubt", "error", "stuck", "solve", "solution needed"]):
                continue  # skip unhelpful posts

            if not any(good in title for good in ["editorial", "explanation", "approach", "tutorial"]):
                continue  # skip irrelevant ones

            topic_id = topic.get("id")
            slug = topic.get("slug")
            topic_url = f"{base_url}/t/{slug}/{topic_id}"

            topic_res = requests.get(f"{base_url}/t/{topic_id}.json", headers=headers)
            topic_json = topic_res.json()

            post_stream = topic_json.get("post_stream", {}).get("posts", [])
            if not post_stream:
                continue

            first_post = post_stream[0]
            cooked = first_post.get("cooked", "")
            soup = BeautifulSoup(cooked, "html.parser")
            text = soup.get_text().strip()

            posts.append({
                "title": topic.get("title"),
                "url": topic_url,
                "text": text[:1200]
            })

        return {
            "problem_code": problem_code,
            "count": len(posts),
            "posts": posts
        }

    except Exception as e:
        return {
            "problem_code": problem_code,
            "count": 0,
            "posts": [],
            "error": str(e)
        }