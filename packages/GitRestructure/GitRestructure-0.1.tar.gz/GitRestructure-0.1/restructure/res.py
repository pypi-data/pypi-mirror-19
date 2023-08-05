import click
import sys
from branchoperator import BranchOperator
import time
import webbrowser

FOXHOUND = 'foxhound'
DEMETER = 'demeter'

# A customized branching helper for Foxhound and Scrummy Bears
@click.command()
@click.argument('branch_type_or_cmd') # this could be a branch type or a git command
@click.argument('action', required=False)
@click.argument('branch-name', required=False)
def cli(branch_type_or_cmd, action, branch_name):

    if branch_name == None:
        branch_name = "ptp-" + time.strftime("%Y/%m/%d")

    operator = BranchOperator()
    if operator.isInsideGitWorkTree() == "False":
        print('you need to be inside a git repo to use this tool')
        return
        
    if branch_type_or_cmd == 'ci' or branch_type_or_cmd == 'commit':
        operator.commit(action)
    elif branch_type_or_cmd == 'add':
        operator.addFiles(action)
    elif 'fox' in branch_type_or_cmd:
        startOperation(branch_type_or_cmd, action, branch_name, FOXHOUND)
    elif 'dem' in branch_type_or_cmd:
        startOperation(branch_type_or_cmd, action, branch_name, DEMETER)
    else:
        print('branch type doesn\'t exist: ' + branch_type_or_cmd)

def startOperation(branch_type, branch_action, branch_name, team):
    operator = BranchOperator()
    if 'feature' in branch_type:
        operator.feature(branch_action, branch_name, team)
    elif 'hotfix' in branch_type:
        operator.branchoperator.hotfix(branch_action, branch_name, team)
    elif 'release' in branch_type:
        operator.release(branch_action, branch_name, team)
    else:
        print("branch type doesn't exist: " + branch_type)
