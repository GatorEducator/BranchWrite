import github
import os
import base64
import sys

TOKEN = os.environ["GITHUB_TOKEN"]
CUR_REPO = os.environ["GITHUB_REPOSITORY"]
OWNER = os.environ["GITHUB_REPOSITORY_OWNER"]



AUTHENTICATED_API = github.Github(TOKEN)


class BranchWrite:
    """target branch."""

    def __init__(self, branch_name="insight", des_path = ".") -> None:
        """initialize the wanted branch if it doesn't exist yet."""
        self.repo_obj = AUTHENTICATED_API.get_repo(CUR_REPO)
        self.insight_branch = branch_name
        self.ref = "refs/heads/" + branch_name
        self.des_path = des_path

        # Get default branch for the use of branch sha
        self.default_branch = (
            AUTHENTICATED_API.get_repo(CUR_REPO).default_branch
        )
        self.default_branch_obj = self.repo_obj.get_branch(self.default_branch)

        # Check if the wanted branch exists or not.
        found_insight_branch = False
        for branch in self.repo_obj.get_branches():
            if branch.name == branch_name:
                found_insight_branch = True
        # Create the wanted branch if not.
        if not found_insight_branch:
            default_branch_obj = self.repo_obj.get_branch(self.default_branch)
            self.repo_obj.create_git_ref(self.ref, sha=default_branch_obj.commit.sha)

    def from_string(self,content):
        """Upload the content to a specific path in the insight branch."""
        self.__write_content(content)
        return

    def from_file(self, source_branch, source_file):
        """Upload content to a specific path in the insight branch from a file in another branch."""
        file = self.repo_obj.get_contents(source_file, ref=source_branch)
        content = base64.b64decode(file.content)
        self.__write_content(content)
        return

    def from_env(self, env):
        """Upload content to a specific path in the insight branch from a environment variable."""
        content = os.getenv(env)
        if not content:
            raise ValueError(f"Can't find {env}, exit the program.")
        self.__write_content(content)
        return

    def __write_content(self,content):
        """Write a file in the destination insight with the given content."""
        # If fails to find the path, create one.
        try:
            file = self.repo_obj.get_contents(self.des_path, ref=self.insight_branch)
            self.repo_obj.update_file(
                path=self.des_path,
                message="upload from action",
                content=content,
                branch=self.insight_branch,
                sha=file.sha,
            )
            print("🚀 successfully updated a file!")
        except github.GithubException:
            self.repo_obj.create_file(
                path=self.des_path,
                message="insight upload",
                content=content,
                branch=self.insight_branch,
            )
            print("🚀 successfully created a file!")

def main():
    args = sys.argv
    expected_arg_amount = 5
    if len(args) != expected_arg_amount:
        raise ValueError(f"5 arguments are expected, {expected_arg_amount - len(args)} from it")
    branch_name = args[1]
    target_path = args[2]
    target_branch = BranchWrite(branch_name, target_path)


    # args[3] decides which function to use and has three options: content, branch-and-file, env
    source = args[3]
    if source == "content":
        content = args[4]
        target_branch.from_string(content)

    elif source == "branch-and-path":
        source_branch, source_path = args[4].split("/")[0], "/".join(args[4].split("/")[1:])
        target_branch.from_file(source_branch,source_path)
    
    elif source == "env":
        env = args[4]
        target_branch.from_env(env)
        
    else:
        raise ValueError("the 3rd positional argument receives unexpected value other than env, content or branch-and-path.")
        

        
        

    
if __name__ == "__main__":
    main()
