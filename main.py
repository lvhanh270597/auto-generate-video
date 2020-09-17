from app.init import Initializer
from app.sync_data import SyncData
from app.preprocess import Preprocessing
from app.process import Processing

class App :

    def __init__(self):
        Initializer()
    
    def process(self) :
        sync = SyncData()
        sync.run()
        preprocess = Preprocessing()
        success, total = preprocess.run()
        print("Preprocessing: Success/Total: {0}/{1}".format(success, total))
        process = Processing()
        success = process.run()
        print("Processing: {0} is created!".format(success))

app = App()
app.process()