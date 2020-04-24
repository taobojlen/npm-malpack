# npm malicious packages

Reads the npm advisories API and gets a list of malicious packages.

Uses [a bit of a hack](https://npm.community/t/can-i-query-npm-for-all-advisory-information/2096/7) to get the API, but that seems to be the recommended way to do it.

When run, `malpack.py` saves a file called `malicious_packages.json` with a JSON list of all advisories titled "malicious package".
