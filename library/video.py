from library.executor import executor
from library.timer import Timer
import os

class VideoInfo :
    
    program = 'ffmpeg'    
    commands = {
        'getInfo' : '{0} -i {1}',
        'reduceVideo' : '{0} -ss 00:00:00 -i {1} -t {2} -vcodec copy -acodec copy {3}',
        'combineAudio' : '{0} -i {1} -i {2} -c:v copy -c:a aac {3}',
        'muteAudio' : '{0} -i {1} -c copy -an {2}',
        'scale' : '{0} -i {1} -vf scale={2} -c:a copy {3}'
    }

    def __init__(self, videoPath):
        self.videoPath = videoPath
    
    def getDuration(self, convertToSeconds=True) :
        command = self.commands['getInfo'].format(
            self.program, 
            self.videoPath
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
    
    def getSAR(self) :
        command = self.commands['getInfo'].format(
            self.program, 
            self.videoPath
        )
        text, _ = executor.runCommand(command)
        SAR = None
        for line in text.splitlines() :
            if line.count('[SAR') :
                SAR = line
                break
        if SAR is None : return None
        start = SAR.index('[SAR ')
        end   = SAR.index(']', start) 
        SAR   = SAR[start: end + 1].strip()
        return SAR.split()[1].strip()

    def reduceVideo(self, lastSeconds, outputPath, overWrite=True, removeOld=False) :
        lengthOfVideo = self.getDuration()
        lengthOfVideo -= lastSeconds
        lengthOfVideo = Timer().convertToString(lengthOfVideo)
        if overWrite :
            if os.path.isfile(outputPath) :
                os.remove(outputPath)
        command = self.commands['reduceVideo'].format(
            self.program, 
            self.videoPath,
            lengthOfVideo,
            outputPath
        )
        _, exitCode = executor.runCommand(command)
        success = (exitCode == 0)
        if success and removeOld : 
            os.remove(self.videoPath)
        return success
    
    def combineAudio(self, audioPath, outputPath, overWrite=True, removeOld=False):
        if overWrite :
            if os.path.isfile(outputPath) :
                os.remove(outputPath)
        command = self.commands['combineAudio'].format(
            self.program, 
            self.videoPath,
            audioPath,
            outputPath
        )
        _, exitCode = executor.runCommand(command)
        success = (exitCode == 0)
        if success and removeOld : 
            os.remove(self.videoPath)
        return success

    def scale(self, scaleSize, outputPath, overWrite=True, removeOld=False):
        if overWrite :
            if os.path.isfile(outputPath) :
                os.remove(outputPath)
        command = self.commands['scale'].format(
            self.program, 
            self.videoPath,
            scaleSize,
            outputPath
        )
        _, exitCode = executor.runCommand(command)
        success = (exitCode == 0)
        if success and removeOld : 
            os.remove(self.videoPath)
        return success

    def muteAudio(self, outputPath, overWrite=True, removeOld=False) :
        if overWrite :
            if os.path.isfile(outputPath) :
                os.remove(outputPath)
        command = self.commands['muteAudio'].format(
            self.program, 
            self.videoPath,
            outputPath
        )
        _, exitCode = executor.runCommand(command)
        success = (exitCode == 0)
        if success and removeOld : 
            os.remove(self.videoPath)
        return success
    
class Videos :

    program = 'ffmpeg'    
    commands = {
        'mergeVideo' : '{0} {1} -filter_complex [0:v][1:v]concat=n={2}:v=1 {3}',
    }

    def __init__(self, listPaths) :
        self.listPaths = listPaths
    
    def mergeVideos(self, outputPath, overWrite=True, removeOld=False) :
        if overWrite :
            if os.path.isfile(outputPath) :
                os.remove(outputPath)
        listFiles = " ".join(
            ["-i {0}".format(item) for item in self.listPaths ]
        )
        command = self.commands['mergeVideo'].format(
            self.program, 
            listFiles,
            len(self.listPaths),
            outputPath
        )
        _, exitCode = executor.runCommand(command)
        success = (exitCode == 0)
        if success and removeOld : 
            for item in self.listPaths : 
                os.remove(item)
        return success
