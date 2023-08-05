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
import sys
from branchoperator import BranchOperator
import time
import webbrowser
from printer import Printer

FOXHOUND = 'foxhound'
DEMETER = 'demeter'

@click.command()
@click.argument('branch_type_or_cmd', required=True) # this could be a branch type or a git command
@click.argument('action', required=False)
@click.argument('provided_name', required=False)
@click.argument('tag_message', required=False)
def cli(branch_type_or_cmd, action, provided_name, tag_message):
    """**************************************************************************
    
    \b
    GBRestructure
        A tool to help with multi-team Git branching strategies

    \b
    Key:
    <team> = shortname for development team
    <tag-name> = the name of a tag.  E.g. v2.4

    \b 
    Feature Branches:
        - Start a feature branch:
            - $gb <team>feature start feature-name
            - Must be started off of team dev branch
        - Finish a feature branch:
            - $gb <team>feature finish

    \b
    Release Branches:
        - Start a release branch:
            - $gb <team>release start release-name
            - Must be started off of a team dev branch
        - Finish a release branch:
            - $gb <team>release finish <tag-name> "tag message"
            - for example $gb demrelease finish v1.3 "version 1.3"

    \b 
    Hotfix Branches:
        - Start a hotfix branch:
            - $gb <team>hotfix start hotfix-name
            - Must be started off of master
        - Finish a hotfix branch:
            - $gb <team>hotfix finish

    \b
    Stage Files:
        - $gb add .
        - $gb add file.txt

    \b
    Commit:
        - $gb commit 'commit message'
        - $gb ci 'commit message'

    \b
    Update Feature Branches:
        - $gb udpate
        - This will pull from master and correct team branch for an update. 

    \b
    Push:
        - $gb push
        - This will push your changes to the working branche's remote

    **************************************************************************"""
    operator = BranchOperator()
    printer = Printer()

    if provided_name == None:
        provided_name = "ptp-" + time.strftime("%Y/%m/%d")
        
    if branch_type_or_cmd == 'ci' or branch_type_or_cmd == 'commit':
        operator.commit(action)
    elif branch_type_or_cmd == 'add':
        operator.addFiles(action)
    elif branch_type_or_cmd == 'update':
        operator.updateCurrentBranch()
    elif branch_type_or_cmd == 'push':
        operator.push()
    elif 'fox' in branch_type_or_cmd:
        startOperation(branch_type_or_cmd, action, provided_name, tag_message, FOXHOUND)
    elif 'dem' in branch_type_or_cmd:
        startOperation(branch_type_or_cmd, action, provided_name, tag_message, DEMETER)
    else:
        printer.showError('branch type or command doesn\'t exist: ' + branch_type_or_cmd)

def startOperation(branch_type, branch_action, branch_name, tag_message, team):
    operator = BranchOperator()
    checkForErrors(operator)

    if 'feature' in branch_type:
        operator.feature(branch_action, branch_name, team)
    elif 'hotfix' in branch_type:
        operator.hotfix(branch_action, branch_name, team)
    elif 'release' in branch_type:
        operator.release(branch_action, branch_name, tag_message, team)
    else:
        printer.showError("branch type doesn't exist: " + branch_type)

def checkForErrors(operator):
    printer = Printer()
    if operator.isInsideGitWorkTree() == False:
        printer.showError('You need to be inside the root folder of a git repo to use GBRestructure')
        sys.exit()

    if operator.repoContainsUnSavedFiles() == True:
        printer.showError("You need to stash your unstaged changes before proceeding")
        sys.exit()

    
