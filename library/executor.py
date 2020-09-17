import subprocess


class BashExecutor :
    def runCommand(self, command) :
        command = command.split()
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        text = result.communicate()[0]
        exitCode = result.returncode
        text = text.decode('utf-8')
        return text, exitCode

executor = BashExecutor()