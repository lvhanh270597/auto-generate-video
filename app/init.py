import os, shutil
from library.timer import Timer
from config.config import config


class Initializer :

    videoStructure = {
        'raw' : { 'files' : 'files.txt' },
        'preprocessed' : {},
        'done'  :  {},
        'trash' :  {},
        'temp'  :  {}
    }

    def __init__(self):
        today = Timer().getTodayString()
        videoPath = os.path.join(config['Local']['videoPath'], today)
        if not os.path.isdir(videoPath) :
            os.makedirs(videoPath)
        for key, val in self.videoStructure.items() :
            currentPath = os.path.join(videoPath, key)
            if not os.path.isdir(currentPath) :
                os.makedirs(currentPath)
            if 'files' in val :
                filePath = os.path.join(currentPath, val['files'])
                if not os.path.isfile(filePath) :
                    f = open(filePath, 'w'); f.close()
                    
