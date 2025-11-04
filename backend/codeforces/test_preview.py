import requests

# Test the API and show a nice preview
url = "http://127.0.0.1:8000/fetch/editorial"
params = {"problem_url": "https://codeforces.com/contest/1741/problem/B"}

print("Fetching editorial...")
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    print("\n" + "="*80)
    print("PROBLEM:", data["problem_metadata"]["name"])
    print("Contest ID:", data["problem_metadata"]["contestId"])
    print("Index:", data["problem_metadata"]["index"])
    print("Tags:", ", ".join(data["problem_metadata"]["tags"]))
    print("="*80)
    
    print("\n📚 Tutorial Links Found:", len(data["tutorial_links"]))
    for link in data["tutorial_links"]:
        print(f"  - {link}")
    
    print("\n📝 Editorials Found:", len(data["editorials"]))
    
    if data["editorials"]:
        editorial = data["editorials"][0]
        text = editorial["text"]
        
        # Show first 1500 characters
        print("\n" + "-"*80)
        print("EDITORIAL PREVIEW (First 1500 characters):")
        print("-"*80)
        print(text[:1500])
        print("-"*80)
        print(f"\n✓ Total length: {len(text)} characters")
        print(f"✓ Lines: {len(text.split(chr(10)))}")
        print("\nThe editorial text has been cleaned and is now readable!")
else:
    print(f"Error: Status code {response.status_code}")
