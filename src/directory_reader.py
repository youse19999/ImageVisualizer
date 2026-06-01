import os 

class IV_Dirs:
    def __init__(self,path):
        self.path = path
        self.files = None
    def get_img_files(self):
        dirs = os.listdir(self.path)
        self.files = dirs
    def get_files(self):
        if self.files == None:
            self.get_img_files()
        return self.files