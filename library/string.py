import random
import string

class String :

    def splitFilename(self, filename) :
        items = filename.split('.')
        filename, ext = '.'.join(items[:-1]), items[-1]
        return filename, ext

    def getRandomString(self, length=8):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str