class Printer(object):

    def failOnWrongAction(self, branch_type, branch_action):
        print('This action doesn\'t exist for ' + branch_type + ' branches: ' + branch_action)

    def printConsiderFeatureFinishedMessage(self, branch_type):
        print('Consider the ' + branch_type + ' finished.  Make sure to finish the pull request')
