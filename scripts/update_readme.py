import os

TEMPLATE_PATH = "templates/profile_template.svg"
OUTPUT_SVG_PATH = "profile_repo/profile.svg"

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def write_svg(content):
    with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
        f.write(content)

def get_github_stats():
    repos = os.getenv("REPO_COUNT", "...")
    stars = os.getenv("STAR_COUNT", "...")
    commits = os.getenv("COMMIT_COUNT", "...")

    return repos, stars, commits

def main():
    template = load_template()
    repos, stars, commits = get_github_stats()

    # 치환
    output = (
        template
        .replace("{{REPOS}}", repos)
        .replace("{{STARS}}", stars)
        .replace("{{COMMITS}}", commits)
    )

    write_svg(output)
    print("SVG updated successfully.")

if __name__ == "__main__":
    main()
