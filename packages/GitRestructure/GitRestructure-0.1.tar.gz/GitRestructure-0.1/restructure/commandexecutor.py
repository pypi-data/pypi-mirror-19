import subprocess

class CommandExecutor(object):

    def execute(self, command):
        subprocess.call([command], shell=True)

    def getReturnValueFromBash(self, command):
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    def getCurrentBranch(self):
        return self.getReturnValueFromBash('git status').communicate()[0].split('On branch ', 1)[1].split('\n', 1)[0]

    def getPullRequestUrl(self, branch_type, branch_action, branch_name, team):
        remote = self.getReturnValueFromBash('git remote -v').communicate()[0].split()[1]
        branch = self.getCurrentBranch()

        compareBranch = ''
        if team == 'foxhound':
            compareBranch = 'foxhound-dev'
        elif team == 'demeter':
            compareBranch = 'demeter-dev'
        else:
            compareBranch = 'master'

        if '@' in remote:
            baseUrl = remote.split('@')[1].rsplit('.', 1)[0].replace(':', '/')
            pullRequestUrl = 'https://' + baseUrl + '/compare' + '/' + compareBranch + '...' + branch
            return pullRequestUrl

        else:
            print('This must be auth by http, I\'m not set up for this.  Set up an ssh key for git access')

    def buildBranchName(self, action, team, name):
        return action + '/' + team  + '/' + name

    def finishBranch(self):
        print('finishing branch')
        currentWorkingBranch = self.getCurrentBranch()
        self.execute('git fetch')
        self.execute('git checkout master')
        self.execute('git pull origin master')
        self.execute('git checkout ' + currentWorkingBranch)
        self.execute('git merge master')
        self.execute('git push')

    def createReleaseBranch(self, name, team):
        print('creating release branch')
        self.createBranchFor('release', name, team)

    def createFeatureBranch(self, name, team):
        print('creating feature branch')
        self.createBranchFor('feature', name, team)

    def createHotfixBranch(self, name, team):
        print('creating hotfix branch')
        branchName = self.buildBranchName('hotfix', team, name)
        self.execute('git fetch')
        self.execute('git pull origin master')
        self.execute('git checkout -b ' + branchName)
        self.execute('git push --set-upstream origin ' + branchName)

    def createBranchFor(self, branch_type, name, team):
        branchName = self.buildBranchName(branch_type, team, name)
        self.execute('git fetch')
        self.execute('git checkout master')
        self.execute('git pull origin master')
        self.execute('git checkout ' + team + '-dev')
        self.execute('git pull origin ' + team + '-dev')
        self.execute('git merge master')
        self.execute('git checkout -b ' + branchName)
        self.execute('git push --set-upstream origin ' + branchName)

    def addFiles(self, files_to_add):
        self.execute('git add ' + files_to_add)

    def commit(self, message):
        self.execute('git commit -m \"' + message + '\"')

    def isInsideGitWorkTree(self):
        return self.getReturnValueFromBash('[ -d .git ] && echo "True" || echo "False"').communicate()[0].replace('\n','')
