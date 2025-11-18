import os
from datetime import datetime

TEMPLATE_PATH = "templates/profile_template.txt"
ASCII_PATH = "templates/ascii_pnow7.txt"
README_PATH = "../README.md"

def load_ascii():
    with open(ASCII_PATH, "r", encoding="utf-8") as f:
        return f.read()

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def write_readme(content):
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

def get_github_stats():
    repos = os.getenv("REPO_COUNT", "...")
    stars = os.getenv("STAR_COUNT", "...")
    commits = os.getenv("COMMIT_COUNT", "...")

    return repos, stars, commits

def main():
    ascii_art = load_ascii()
    template = load_template()
    repos, stars, commits = get_github_stats()

    # 템플릿 치환
    output = (
        template
        .replace("{{ASCII_ART}}", ascii_art)
        .replace("{{REPOS}}", repos)
        .replace("{{STARS}}", stars)
        .replace("{{COMMITS}}", commits)
    )

    write_readme(output)
    print("README updated successfully.")

if __name__ == "__main__":
    main()
