import requests
from tqdm import tqdm
import json

PAGE_SIZE = 100
BASE_URL = "https://www.npmjs.com/advisories?perPage={}".format(PAGE_SIZE)

# Some titles have weird unicode chars, e.g.
# "Malicious \udb40\udd6e\udb40\udd70\udb40\udd6dPackage"
# so we just take ASCII
def to_ascii(s: str):
  return "".join(c for c in s if ord(c)<128)

def get_page(page: int):
  r = requests.get("{}&page={}".format(BASE_URL, page), headers={"X-Spiferack": "1"})
  return r.json()

def get_malicious_packages():
  next_page = 0
  malicious_packages = []
  print("Starting...")
  t = tqdm()
  while next_page >= 0:
    page = get_page(next_page)
    advisories = page["advisoriesData"]["objects"]
    mal = [advisory for advisory in advisories if to_ascii(advisory["title"]).lower() == "malicious package"]
    malicious_packages.extend(mal)

    if not 'total_advisories' in locals():
      total_advisories = page["advisoriesData"]["total"]
      t.total = total_advisories
      t.refresh()

    t.update(len(advisories))

    # If there are more pages, continue
    if "next" in page["advisoriesData"]["urls"]:
      next_page += 1
    else:
      break

  t.close()
  return malicious_packages

if __name__ == "__main__":
  malicious_packages = get_malicious_packages()
  print("Found {} malicious package advisories.".format(len(malicious_packages)))
  with open("malicious_packages.json", "w") as f:
    json.dump(malicious_packages, f, indent=4)
