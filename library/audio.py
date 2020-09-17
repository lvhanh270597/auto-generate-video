from library.executor import executor
from library.timer import Timer
import random
import os

class AudioInfo :
    
    program = 'ffmpeg'    
    commands = {
        'getInfo' : '{0} -i {1}',
        'getSub' : '{0} -ss {1} -i {2} -t {3} -vcodec copy -acodec copy {4}'
    }

    def __init__(self, audioPath):
        self.audioPath = audioPath
    
    def getDuration(self, convertToSeconds=True) :
        command = self.commands['getInfo'].format(
            self.program, 
            self.audioPath
        )
        text, _ = executor.runCommand(command)
        duration = None
        for line in text.splitlines() :
            line = line.strip()
            if line.startswith('Duration:') :
                duration = line
                break
        if duration is None : return None
        duration = duration.split(',')[0]
        duration = duration.split()[-1]
        if convertToSeconds :
            hours, minutes, seconds = list(map(float, duration.split(':')))
            duration = hours * 3600 + minutes * 60 + seconds
        return duration

    def getWithLength(self, lengthBySeconds, outputPath, overWrite=True) :
        lengthOfVideo, lengthBySeconds = int(self.getDuration()), int(lengthBySeconds)
        start = random.randint(0, lengthOfVideo - lengthBySeconds)
        lengthBySeconds = Timer().convertToString(lengthBySeconds)
        start = Timer().convertToString(start)
        if overWrite :
            if os.path.isfile(outputPath) :
                os.remove(outputPath)
        command = self.commands['getSub'].format(
            self.program, 
            start,
            self.audioPath,
            lengthBySeconds,
            outputPath
        )
        text, exitCode = executor.runCommand(command)
        return exitCode == 0