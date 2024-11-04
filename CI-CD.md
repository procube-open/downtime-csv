# CI-CD

Open your project in CodeSpaces. devcontainer will be automatically started and you should be able to use CI-CD commands.

Tips: 
If you open the terminal immediately after startup, bash will start without loading the poetry virtual environment. In that case, exit and restart bash.

# Release

If you want to release a new version, please commit it with a message in[ Angular commit message style](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits). Then release it with the command below.

```shell
souce .env/bin/activeate
export GH_TOKEN=YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
semantic-release version --patch --vcs-release
```
