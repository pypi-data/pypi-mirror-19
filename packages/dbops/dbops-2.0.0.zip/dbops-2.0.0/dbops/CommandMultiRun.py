import os
import itertools
"""CommandMultiRun:
    Inputs:
        arglst - things to run on
            List should strictly be a list of lists of items.
            Single items should still be in a list.
        command - what to run
            the path to a text file with {n} replacement cues.
        mode - how to handle the output
            "print" for print out, "bash" for run in bash, or a filname"""

class CommandMultiRun(object):

    """Neat Patch Looping. Can be used with BOP."""
    def __init__(self, arglst=[["dog", "cat"],["lemon"]], mode ="print",
                 command="food.pmr"):
        """Take in input."""
        self.list = list
        with open(command, 'r') as cmf:
            self.command = cmf.read()
        self.mode = mode

    def replace(self, inputs):
        """Replace {x} with a list of inputs."""
        return self.command.format(*inputs)

    def output(self, result, mode="print"):
        """Do what is expected with the commands as they come."""
        if mode == "print":
            print(result)
        elif mode == "bash":
            os.system(result)
        else:
            # mode is a filename to try to write to
            with open(mode, 'a') as outfile:
                outfile.write(result+"\n")

    def run(self):
        """Run through the list and format and run commands."""
        for arglist in itertools.product(*self.arglst):
            self.output(self.replace(arglist))


if __name__ == "__main__":
    """Run from command line."""
    import sys
    args = ['nothing', '[[1],[2,3]]', 'print, ''food.pmr']
    for x in range(1, len(sys.argv)):
        args[x] = sys.argv[x]
    runner = CommandMultiRun(args[1], args[2], args[3])
    runner.run()
