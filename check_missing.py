import csv
import json

# Load packages in backstabber dataset
backstabber_packages = set()
with open("package_index.csv", "r") as idx_file:
    reader = csv.DictReader(idx_file, delimiter=",")
    for row in reader:
        if row["Type"] == "npm":
            backstabber_packages.add(row["Package Name"])

# Load packages from npm
with open("malicious_packages.json", "r") as npm_file:
    packages_json = json.load(npm_file)
    npm_packages = set([p["module_name"] for p in packages_json])

    missing = list(npm_packages.difference(backstabber_packages))
    print("\n".join(missing))

    # Save details of missing packages
    details = [p for p in packages_json if p["module_name"] in missing]
    with open("missing.json", "w") as missing_file:
        json.dump(details, missing_file, indent=4)
