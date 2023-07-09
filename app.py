import oloren as olo
import ssl
import json
import urllib.request
import urllib.parse
import os


@olo.register(
    description="Use brightdata proxy to convert search queries to JSON. Requires BRIGHT_DATA_HOST, BRIGHT_DATA_USERNAME, BRIGHT_DATA_PASSWORD environment variables to be set."
)
def brightdata_serp(search=olo.String()):
    engine = "https://www.google.com/search"  # can make this parameter once defaults are implemented

    ssl._create_default_https_context = ssl._create_unverified_context

    BRIGHT_DATA_HOST = os.environ["BRIGHT_DATA_HOST"]
    BRIGHT_DATA_USERNAME = os.environ["BRIGHT_DATA_USERNAME"]
    BRIGHT_DATA_PASSWORD = os.environ["BRIGHT_DATA_PASSWORD"]

    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(
            {
                "http": f"http://{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}@{BRIGHT_DATA_HOST}",
                "https": f"http://{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}@{BRIGHT_DATA_HOST}",
            }
        )
    )
    search = urllib.parse.quote(search)
    return json.loads(opener.open(f"{engine}?q={search}&gl=us&lum_json=1").read())


if __name__ == "__main__":
    olo.run("scraping")
