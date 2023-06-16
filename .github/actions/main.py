import github
import os
import base64
import sys

TOKEN = os.environ["GITHUB_TOKEN"]
CUR_REPO = os.environ["GITHUB_REPOSITORY"]
OWNER = os.environ["GITHUB_REPOSITORY_OWNER"]



AUTHENTICATED_API = github.Github(TOKEN)


class insightBranch:
    """insight branch."""

    def __init__(self, branch_name="insight") -> None:
        """initialize an insight branch if it doesn't exist yet."""
        self.repo_obj = AUTHENTICATED_API.get_repo(CUR_REPO)
        self.insight_branch = branch_name
        self.ref = "refs/heads/insight"
        self.default_branch = (
            AUTHENTICATED_API.get_repo(CUR_REPO).default_branch
        )

        self.default_branch_obj = self.repo_obj.get_branch(self.default_branch)
        # Check if insight branch exists or not.
        found_insight_branch = False
        for branch in self.repo_obj.get_branches():
            if branch.name == branch_name:
                found_insight_branch = True

        # Create insight branch if not.
        if not found_insight_branch:
            default_branch_obj = self.repo_obj.get_branch(self.default_branch)
            self.repo_obj.create_git_ref(self.ref, sha=default_branch_obj.commit.sha)

    def content_upload_from_string(self, path,user_content):
        """Upload the content to a specific path in the insight branch."""

        # If fails to find the path, create one.
        try:
            file = self.repo_obj.get_contents(path, ref=self.insight_branch)
            # TODO: avoid updating while the content doesn't change
            self.repo_obj.update_file(
                path=path,
                message="insight upload",
                content=user_content,
                branch=self.insight_branch,
                sha=file.sha,
            )
            print("🚀 successfully updated a file!")
        except github.GithubException:
            self.repo_obj.create_file(
                path=path,
                message="insight upload",
                content=user_content,
                branch=self.insight_branch,
            )
            print("🚀 successfully created a file!")

    def content_upload_from_file(self, path, source_branch, source_file):
        """Upload content to a specific path in the insight branch from a file in another branch."""

        if not source_branch:
            source_branch = self.default_branch
        file = self.repo_obj.get_contents(source_file, ref=source_branch)
        user_content = base64.b64decode(file.content)
        # If fails to find the path, create one.
        try:
            file = self.repo_obj.get_contents(path, ref=self.insight_branch)
            self.repo_obj.update_file(
                path=path,
                message="insight upload",
                content=user_content,
                branch=self.insight_branch,
                sha=file.sha,
            )
            print("🚀 successfully updated a file!")
        except github.GithubException:
            self.repo_obj.create_file(
                path=path,
                message="insight upload",
                content=user_content,
                branch=self.insight_branch,
            )
            print("🚀 successfully created a file!")

def main():
    args = sys.argv
    branch_name = args[1]
    target_branch = insightBranch(branch_name)
    target_path = args[2]

    # args[3] decides which function to use and has three options: content, branch-and-file, env
    source = args[3]
    if source == "content":
        content = args[4]
        target_branch.content_upload_from_string(target_path,content)
    elif source == "branch-and-path":
        source_branch, source_path = args[4].split("/")[0], "/".join(args[4].split("/")[1:])
        target_branch.content_upload_from_file(target_path,source_branch,source_path)
    
    else:
        print("env will come in the future")
        

        
        

    
if __name__ == "__main__":
    main()
