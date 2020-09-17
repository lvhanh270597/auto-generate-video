#!/usr/bin/python3
import os, shutil, random
from config.config import config
from library.timer import Timer
from library.video import VideoInfo
from library.video import Videos
from library.audio import AudioInfo
from library.string import String

# chon videos co SAR bang nhau de duoc 1 video 5 phut
# cat am de tuong ung voi do dai bang video
# combine am thanh va video de tao ra video moi la ket qua


class Processing :

    def __init__(self):
        localPath = os.path.join(
            config['Local']['videoPath'], 
            Timer().getTodayString()
        )
        self.inputFolder  = os.path.join(localPath, 'preprocessed')
        self.tempFolder   = os.path.join(localPath, 'temp')
        self.trashFolder  = os.path.join(localPath, 'trash')
        self.outputFolder = os.path.join(localPath, 'done')
        self.videoSize    = int(config['Video']['videoSize'])
        self.extensionAllowed = config['Video']['extension'].split(',')
        self.acceptSAR    = config['Video']['acceptSAR'].strip()
        self.outputExtension = 'mp4'
        self.audioFolder  = config['Local']['musicPath']

    def generateAudio(self, length) :
        randomFile = random.choice(os.listdir(self.audioFolder))
        filename, ext = String().splitFilename(randomFile)
        outputPath = os.path.join(
            self.tempFolder,
            "{0}.{1}".format(String().getRandomString(), ext)
        )
        randomFile = os.path.join(self.audioFolder, randomFile)
        audio = AudioInfo(randomFile)
        audio.getWithLength(length, outputPath)
        return outputPath

    def processList(self, listPaths, length) :
        videos = Videos(listPaths)
        tempPath = os.path.join(self.tempFolder, "{0}.{1}".format(
            String().getRandomString(), 
            self.outputExtension
        ))
        videos.mergeVideos(tempPath, removeOld=True)
        audioPath = self.generateAudio(length)
        outputPath = os.path.join(self.outputFolder, "{0}.{1}".format(
            String().getRandomString(), 
            self.outputExtension
        ))
        video = VideoInfo(tempPath)
        return video.combineAudio(audioPath, outputPath) 

    def clean(self) :
        for item in os.listdir(self.tempFolder) :
            currentPath = os.path.join(self.tempFolder, item)
            os.remove(currentPath)

    def run(self) :
        self.clean()
        success, currentLength, currentFiles = 0, 0, []
        for item in os.listdir(self.inputFolder) :
            filename, ext = String().splitFilename(item)
            if ext not in self.extensionAllowed : continue
            filePath = os.path.join(self.inputFolder, item)
            video = VideoInfo(filePath)
            if video.getSAR() != self.acceptSAR :
                trashPath = os.path.join(self.trashFolder, item)
                shutil.move(filePath, trashPath)
                continue
            currentLength += video.getDuration()
            currentFiles.append(filePath)
            if currentLength >= self.videoSize :
                if self.processList(currentFiles[:], currentLength) : success += 1
                currentLength, currentFiles = 0, []
        return success
