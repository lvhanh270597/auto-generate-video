#!/usr/bin/python3
import os, shutil
from config.config import config
from library.timer import Timer

class SyncData :

    def __init__(self):
        today = Timer().getTodayString()
        self.rawDirectory = os.path.join(config['Local']['videoPath'], today, 'raw')
        self.listFiles = set(open(os.path.join(self.rawDirectory, 'files.txt')).read().splitlines())
        self.internetDirectory = config['Internet']['videoPath']

    def rewriteListFiles(self, newFiles) :
        with open(os.path.join(self.rawDirectory, 'files.txt'), 'a') as fp :
            fp.write("\n".join(newFiles))
            fp.close()

    def run(self) :
        newFiles = []
        for item in os.listdir(self.internetDirectory) :
            success = (item not in self.listFiles)
            if success :
                self.listFiles.add(item)
                newFiles.append(item)
                src = os.path.join(self.internetDirectory, item)
                dst = os.path.join(self.rawDirectory, item)
                shutil.copyfile(src, dst)
        self.rewriteListFiles(newFiles)
