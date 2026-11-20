"""
Pure-Python GitHub Push Engine using Dulwich
Pushes the local commits to: https://github.com/akashreddy5443123/feedback-dashboard.git
"""
import sys
import os
from dulwich import porcelain


def main():
    token = None
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
    elif "GITHUB_TOKEN" in os.environ:
        token = os.environ["GITHUB_TOKEN"].strip()

    if not token:
        print("=" * 60)
        print(" GITHUB AUTHENTICATION REQUIRED")
        print("=" * 60)
        print("All changes are committed locally to Git (Commit 50a9a89).")
        print("To push to GitHub, a Personal Access Token (PAT) is required:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token' (select 'repo' scope)")
        print("3. Run: python push_to_github.py <YOUR_GITHUB_TOKEN>")
        print("=" * 60)
        return

    remote_url = f"https://akashreddy5143123:{token}@github.com/akashreddy5443123/feedback-dashboard.git"
    print("Connecting to GitHub and pushing 'main' branch...")
    try:
        porcelain.push(".", remote_url, "refs/heads/main")
        print("SUCCESS: All commits successfully pushed to https://github.com/akashreddy5443123/feedback-dashboard")
    except Exception as e:
        print(f"Push error: {e}")


if __name__ == "__main__":
    main()
