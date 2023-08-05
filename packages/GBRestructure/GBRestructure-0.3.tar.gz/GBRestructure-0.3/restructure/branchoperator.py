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

import click
import subprocess
import sys
from commandexecutor import CommandExecutor
import webbrowser
import time
from printer import Printer

class BranchOperator(object):

    START = 'start'
    FINISH = 'finish'
    FEATURE = 'feature'
    HOTFIX = 'hotfix'
    RELEASE = 'release'
    FOXHOUND_DEV_BRANCH_NAME = 'foxhound-dev'
    DEMETER_DEV_BRANCH_NAME = 'demeter-dev'
    MASTER = 'master'

    def __init__(self):
        self.commandexecutor = CommandExecutor()
        self.printer = Printer()

    def feature(self, action, name, team):
        if action == None:
            print('You must specify an action when working with a feature')
            return
        currentBranchName = self.commandexecutor.getCurrentBranch()
        if action == self.START:
            if currentBranchName != self.FOXHOUND_DEV_BRANCH_NAME and currentBranchName != self.DEMETER_DEV_BRANCH_NAME:
                print ('you need to be on team dev branch to start a feature')
                return
            elif team not in currentBranchName:
                print('You need to be on the correct team branch to start a ' + team + ' feature')
            else:
                self.commandexecutor.createFeatureBranch(name, team)

        elif action == self.FINISH:
            self.commandexecutor.finishBranch()
            self.openBrowserToPullRequest(self.FEATURE, action, name, team)
            self.printer.printConsiderFeatureFinishedMessage(self.FEATURE)
        else:
            self.printer.failOnWrongAction(self.FEATURE, action)

    def hotfix(self, action, name, team):
        if action == None:
            print('You must specify an action when working with a hotfix')
            return
        if action == self.START:
            if self.commandexecutor.getCurrentBranch() != self.MASTER:
                print ('you need to be on master to start a hotfix')
            else:
                self.commandexecutor.createHotfixBranch(name, team)

        elif action == self.FINISH:
            self.commandexecutor.finishBranch()
            self.openBrowserToPullRequest(self.HOTFIX, action, name, team)
            self.printer.printConsiderFeatureFinishedMessage(self.HOTFIX)
        else:
            self.printer.failOnWrongAction(self.HOTFIX, action)

    def release(self, action, name, tag_message, team):
        if action == None:
            print('You must specify an action when working with a release')
            return
        currentBranchName = self.commandexecutor.getCurrentBranch()
        if action == self.START:
            if currentBranchName != self.FOXHOUND_DEV_BRANCH_NAME and currentBranchName != self.DEMETER_DEV_BRANCH_NAME:
                print ('you need to be on team dev branch to start a release')
            else:
                self.commandexecutor.createReleaseBranch(name, team)

        elif action == self.FINISH:
            success = self.commandexecutor.finishReleaseBranch(name, tag_message)
            if (success):
                self.openBrowserToPullRequest(self.RELEASE, action, name, 'changeThisValueToSomethingThatMakesSense')
                self.printer.printConsiderFeatureFinishedMessage(self.RELEASE)
        else:
            self.printer.failOnWrongAction(self.RELEASE, action)

    def openBrowserToPullRequest(self, branch_type, action, name, team):
        print('waiting for git repo to sync....')
        time.sleep(3.5)
        pullRequestUrl = self.commandexecutor.getPullRequestUrl(branch_type, action, name, team)
        webbrowser.open(pullRequestUrl)

    def addFiles(self, files_to_add):
        if files_to_add != None:
            self.commandexecutor.addFiles(files_to_add)
        else:
            print('You need to tell me which files to stage')

    def commit(self, message):
        if message != None:
            self.commandexecutor.commit(message)
        else:
            print('Please specify a commit message')

    def isInsideGitWorkTree(self):
        if self.commandexecutor.isInsideGitWorkTree() == 'True':
            return True
        else:
            return False

    def repoContainsUnSavedFiles(self):
        return self.commandexecutor.repoContainsUnSavedFiles()


    
