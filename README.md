# BranchWrite

Write a file on a specific Git branch under the GitHub workflow scenario.

## Premise and Setup

BranchWrite is designed to write contents in the running repository, such that authentication with writing permission is required to put into input arg `repo-token`. It's recommended to use `GITHUB_ACTION` token automatically generated by GitHub Action and enable write contents permission for it. FO more information about `GITHUB_ACTION`, please visit the [github doc](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)

## Usage

see [action.yml](action.yml)

### Example

#### content
```yaml
- name: 
uses: GatorEducator/BranchWrite@v1
if:
    always()
with:
    repo-token: ${{ secrets.GITHUB_TOKEN }}
    branch: insight
    path: cool/insight.json
    source: content
    source-arg: hello from action
```
#### env

```yaml
- name: 
uses: GatorEducator/BranchWrite@v1
if:
    always()
with:
    repo-token: ${{ secrets.GITHUB_TOKEN }}
    branch: insight
    path: cool/insight.json
    source: env
    source-arg: JSON_REPORT
```

#### branch + file

```yaml
- name: 
uses: GatorEducator/BranchWrite@v1
if:
    always()
with:
    repo-token: ${{ secrets.GITHUB_TOKEN }}
    branch: insight
    path: cool/insight.json
    source: branch-and-path
    source-arg: main-branch/foo/bar.txt
```
## License

The scripts and documentation in this project are released under the [MIT License](LICENSE)
