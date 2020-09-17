#!/usr/bin/python3
import os, shutil
from config.config import config
from library.timer import Timer
from library.video import VideoInfo
from library.string import String

# Tat am
# Cat 4s cuoi
# Scale to ra
# Chuyen vao preprocessed

class Preprocessing :

    def __init__(self):
        localPath = os.path.join(
            config['Local']['videoPath'], 
            Timer().getTodayString()
        )
        self.inputFolder  = os.path.join(localPath, 'raw')
        self.tempFolder   = os.path.join(localPath, 'temp')
        self.outputFolder = os.path.join(localPath, 'preprocessed')
        self.lastSeconds  = 4
        self.scaleSize = config['Video']['scaleSize']
        self.extensionAllowed = config['Video']['extension'].split(',')
        self.errorFiles = []
    
    def run(self) :
        success, total = 0, 0
        for item in os.listdir(self.inputFolder) :
            filename, ext = String().splitFilename(item)
            if ext not in self.extensionAllowed : continue
            currentSuccess, total = False, total + 1
            filePath = os.path.join(self.inputFolder, item)
            tempPath = os.path.join(self.tempFolder, item)
            outputPath = os.path.join(self.outputFolder, item)
            videoInfo = VideoInfo(filePath)
            if videoInfo.muteAudio(tempPath) :
                _tempName = "{0}_1.{1}".format(filename, ext)
                _tempPath = os.path.join(self.tempFolder, _tempName)
                videoInfo = VideoInfo(tempPath)
                if videoInfo.reduceVideo(self.lastSeconds, _tempPath) :
                    __tempName = "{0}_2.{1}".format(filename, ext)
                    __tempPath = os.path.join(self.tempFolder, __tempName)
                    videoInfo = VideoInfo(_tempPath)
                    if videoInfo.scale(self.scaleSize, __tempPath) :
                        currentSuccess, success = True, success + 1
                        shutil.move(__tempPath, outputPath)
                    os.remove(_tempPath)
                os.remove(tempPath)
            if currentSuccess : os.remove(filePath)
            else : self.errorFiles.append(item)
        return (success, total)

