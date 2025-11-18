import os
import requests
from datetime import datetime
from dateutil import relativedelta

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
USER_NAME = os.environ["USER_NAME"]

headers = {
    "Authorization": f"token {ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_user():
    url = f"https://api.github.com/users/{USER_NAME}"
    return requests.get(url, headers=headers).json()

def get_repos():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USER_NAME}/repos?per_page=100&page={page}"
        data = requests.get(url, headers=headers).json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_stars(repos):
    return sum(r.get("stargazers_count", 0) for r in repos)

def get_loc(repos):
    total = 0
    for repo in repos:
        if not repo["fork"]:
            url = f"https://api.github.com/repos/{USER_NAME}/{repo['name']}/languages"
            lang_data = requests.get(url, headers=headers).json()
            total += sum(lang_data.values())
    return total

def format_uptime(created_at):
    created = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.utcnow()
    diff = relativedelta.relativedelta(now, created)
    return f"{diff.years}y {diff.months}m {diff.days}d"

def update_readme():
    user = get_user()
    repos = get_repos()

    stars = get_stars(repos)
    loc = get_loc(repos)
    uptime = format_uptime(user["created_at"])

    languages = set()
    for repo in repos:
        if repo["language"]:
            languages.add(repo["language"])

    # Load template
    with open("templates/profile_template.txt", "r", encoding="utf-8") as f:
        template = f.read()

    profile_text = template.format(
        USER=USER_NAME,
        OS="Windows 11",
        UPTIME=uptime,
        REPOS=user["public_repos"],
        FOLLOWERS=user["followers"],
        STARS=stars,
        LOC=f"{loc:,}",
        LANGUAGES=", ".join(languages)
    )

    # Write to README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(profile_text)

if __name__ == "__main__":
    update_readme()
