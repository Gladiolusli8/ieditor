from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog
import os
from PIL import Image, ImageFilter

window = QApplication([])
window_m = QWidget()
window_m.setWindowTitle('Gladiolus_li8 image editor')
window_m.resize(700, 500)
foldr = QPushButton('Папка')
pic = QLabel('Картинка')
lst = QListWidget()
lft = QPushButton('Лево')
rght = QPushButton('Право')
mrrr = QPushButton('Зеркало')
chb = QPushButton('ЧБ')
rskost = QPushButton('Резкоcть')
row = QHBoxLayout()
col = QVBoxLayout()
col0 = QVBoxLayout()
col.addWidget(foldr)
col.addWidget(lst)
col0.addWidget(pic, 95)
row_t = QHBoxLayout()
row_t.addWidget(lft)
row_t.addWidget(rght)
row_t.addWidget(mrrr)
row_t.addWidget(chb)
row_t.addWidget(rskost)
col0.addLayout(row_t)
row.addLayout(col, 20)
row.addLayout(col0, 80)
window_m.setLayout(row)
wrkdr = ''
def chswordr():
    global wrkdr
    wrkdr = QFileDialog.getExistingDirectory()
#   wrkdr = QFileDialog.getOpenFileName()
def fltr(fles, extnsns):
    rslt = []
    for filename in fles:
        for ext in extnsns:
            if filename.endswith(ext):
                rslt.append(filename)
    return rslt
def shwflnslst():
    extnsns = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chswordr()
    flns = fltr(os.listdir(wrkdr), extnsns)
    lst.clear()
    for filename in flns:
        lst.addItem(filename)
foldr.clicked.connect(shwflnslst)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.mod = 'Modified/'
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        imagepath = os.path.join(dir, filename)
        self.image = Image.open(imagepath)
    def showimage(self, path):
        pic.hide()
        pixmapimage = QPixmap(path)
        w, h = pic.width(), pic.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        pic.setPixmap(pixmapimage)
        pic.show()
    def bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(wrkdr, self.mod, self.filename)
        self.showimage(image_path)
    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(wrkdr, self.mod, self.filename)
        self.showimage(image_path)
    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(wrkdr, self.mod, self.filename)
        self.showimage(image_path)
    def flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(wrkdr, self.mod, self.filename)
        self.showimage(image_path)
    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(wrkdr, self.mod, self.filename)
        self.showimage(image_path)
    def saveImage(self):
        path = os.path.join(wrkdr, self.mod)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        
workimage = ImageProcessor()
def showchoosenimage():
    if lst.currentRow() >= 0:
        filename = lst.currentItem().text()
        workimage.loadImage(wrkdr, filename)
        image_path = os.path.join(wrkdr, workimage.filename)
        workimage.showimage(image_path)
lst.currentRowChanged.connect(showchoosenimage)
chb.clicked.connect(workimage.bw)
rght.clicked.connect(workimage.right)
lft.clicked.connect(workimage.left)
mrrr.clicked.connect(workimage.flip)
rskost.clicked.connect(workimage.sharpen)
window_m.show() 
window.exec_()