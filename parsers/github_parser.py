# parsers/github_parser.py
import requests

def fetch_github_profile(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Failed to fetch GitHub profile for '{username}'. Status code: {response.status_code}")
def fetch_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Failed to fetch GitHub repositories for '{username}'. Status code: {response.status_code}")
    
if __name__ == "__main__":
    profile = fetch_github_profile("Blitzhac")
    print(profile)
    repos = fetch_github_repos("Blitzhac")
    print(repos)