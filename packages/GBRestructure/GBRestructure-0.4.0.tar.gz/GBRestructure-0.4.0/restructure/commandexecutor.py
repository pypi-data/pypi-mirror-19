# Copyright 2017 Josh Fischer

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
from printer import Printer

class CommandExecutor(object):

    def __init__(self):
        self.printer = Printer()

    def execute(self, command):
        subprocess.call(command, shell=True)

    def getReturnValueFromBash(self, command):
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    def getCurrentBranch(self):
        return self.getReturnValueFromBash('git status').communicate()[0].split('On branch ', 1)[1].split('\n', 1)[0]

    def tagAlreadyExists(self, provided_tag_version):
        provided_tag_version = provided_tag_version.lower()
        if 'v' not in provided_tag_version:
            provided_tag_version = 'v' + provided_tag_version
              
        self.execute('git fetch --tags')
        tag_string = self.getReturnValueFromBash('git tag').communicate()[0]
        tag_list = tag_string.split("\n")
        if provided_tag_version in tag_list:
            return True
        else:
            return False


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
        self.execute('git checkout master')
        self.execute('git pull origin master')
        self.execute('git checkout ' + currentWorkingBranch)
        self.execute('git merge master')
        self.execute('git push')

    def finishReleaseBranch(self, tag_version, tag_message):
        if tag_version == None or tag_message == None:
            self.printer.showError('Please specify a version and a custom message for the tag')
            return False

        if self.tagAlreadyExists(tag_version) == True:
            self.printer.showError('tag already exists, pick a different version')
            return False
        
        print('finishing branch')
        currentWorkingBranch = self.getCurrentBranch()
        self.execute('git checkout master')
        self.execute('git pull origin master')
        self.execute('git checkout ' + currentWorkingBranch)
        self.execute('git merge master')
        self.execute('git push')
        self.createAnnotatedTag(tag_version, tag_message)
        return True

    def createReleaseBranch(self, name, team):
        print('creating release branch')
        self.createBranchFor('release', name, team)

    def createFeatureBranch(self, name, team):
        print('creating feature branch')
        self.createBranchFor('feature', name, team)

    def createHotfixBranch(self, name, team):
        print('creating hotfix branch')
        branchName = self.buildBranchName('hotfix', team, name)
        self.execute('git pull origin master')
        self.execute('git checkout -b ' + branchName)
        self.execute('git push --set-upstream origin ' + branchName)

    def createBranchFor(self, branch_type, name, team):
        branchName = self.buildBranchName(branch_type, team, name)
        self.execute('git checkout master')
        self.execute('git pull origin master')
        self.execute('git checkout ' + team + '-dev')
        self.execute('git pull origin ' + team + '-dev')
        self.execute('git merge master')
        self.execute('git checkout -b ' + branchName)
        self.execute('git push --set-upstream origin ' + branchName)

    def updateCurrentBranch(self, team, current_branch):

        self.execute('git checkout master')
        self.execute('git pull origin master')
        self.execute('git checkout ' + team + '-dev')
        self.execute('git pull origin ' + team + '-dev')
        self.execute('git checkout ' + current_branch)
        self.execute('git merge --ff ' + team + '-dev')
        self.execute('git merge --ff master')

    def createAnnotatedTag(self, tag_version, tag_message):
        self.execute('git tag -a v' + tag_version + ' -m \"' + tag_message + '\"')
        self.execute('git push origin ' + tag_version)

    def addFiles(self, files_to_add):
        self.execute('git add ' + files_to_add)

    def commit(self, message):
        self.execute('git commit -m \"' + message + '\"')
        
    def push(self):
        current_branch = self.getCurrentBranch()
        self.execute('git push origin ' + current_branch)

    def isInsideGitWorkTree(self):
        return self.getReturnValueFromBash('[ -d .git ] && echo "True" || echo "False"').communicate()[0].replace('\n','')

    def repoContainsUnSavedFiles(self):
        status_message = self.getReturnValueFromBash("git status").communicate()[0]
        if "nothing to commit" in status_message:
            return False
        else:
           return True

