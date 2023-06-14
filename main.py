import github

import os

# TOKEN = os.environ["GITHUB_TOKEN"]
# CUR_REPO = os.environ["GITHUB_REPOSITORY"]
# OWNER = os.environ["GITHUB_REPOSITORY_OWNER"]

# AUTHENTICATED_API = Github(TOKEN)


CUR_REPO = "hey-you-be-positive"
OWNER = "allegheny-college-sandbox"

AUTHENTICATED_API = github.Github("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")



class insightBranch:
    """insight branch."""
    def __init__(self,branch_name = "insight") -> None:
        """initialize an insight branch if it doesn't exist yet."""
        self.repo_obj = AUTHENTICATED_API.get_organization(OWNER).get_repo(CUR_REPO)
        self.insight_branch = branch_name
        self.ref = ref='refs/heads/' + branch_name

        # Check if insight branch exists or not.
        found_insight_branch = False
        for branch in self.repo_obj.get_branches():
            if branch.name == branch_name:
                found_insight_branch = True
        
        # Create insight branch if not.
        if not found_insight_branch:

            default_branch_name = self.repo_obj.default_branch
            default_branch_obj = self.repo_obj.get_branch(default_branch_name)
            self.repo_obj.create_git_ref(self.ref, sha=default_branch_obj.commit.sha)

    
    def content_upload(self,content, path = "."):
        """Upload the content to a specific path in the insight branch."""

        # If fails to find the path, create one.
        try: 
            file = self.repo_obj.get_contents(path,ref = self.insight_branch)
            print(file.content)
        except github.GithubException:
            self.repo_obj.create_file(path=path, message="insight upload",content="insight is cool",branch=self.insight_branch)
        


if __name__ == "__main__":
    branch = insightBranch()
    branch.content_upload(content= "hello", path="./cool/insight.json")