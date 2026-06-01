from PIL import Image

class IV_Image:
    def __init__(self,path):
        self.img = Image.open(path)
    def get_image(self):
        return self.img
    def get_format(self):
        return self.img.format
    def get_size(self):
        return self.img.size
    def get_mode(self):
        return self.img.mode