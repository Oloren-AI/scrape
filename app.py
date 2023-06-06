import oloren as olo
from serpapi import GoogleSearch


@olo.register(description="Use SERP API to export Google results to JSON")
def scrape_google(api_key=olo.String(secret=True), query=olo.String()):
    params = {
        "q": query,
        "location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": api_key,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    return organic_results


@olo.register(description="Human readable SERP")
def pretty_serp_convert(results=olo.Json()):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ret = []
    for i, result in enumerate(results):
        ret.append(f"{alphabet[i]}) {result['title']} ({result['source']}) - {result['snippet']}")
    return "\n".join(ret)


@olo.register()
def parse_gpt(inp=olo.String()):
    results = []
    for line in inp.split("\n"):
        if "=" in line:
            score, description = line.split("=")[1].strip().split("|")
            results.append({"score": int(score), "description": description})
    return results


if __name__ == "__main__":
    olo.run("scraping")
