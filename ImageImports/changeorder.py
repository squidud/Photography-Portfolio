from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
import sys
import os
import glob

src_dir = os.path.dirname(os.path.abspath(__file__))
dst_dir = os.path.abspath(os.path.join(src_dir, '../Images'))
webp_images = glob.glob(os.path.join(dst_dir, '*.webp'))
ordered_images = []


#TODO: read current order file, transfer to list, for each in images in the folder, if in order file, nothing,
    #if not, add to new photos list. After, listfile + new photos = new default order
    #have converterscript generate html based on ordered list file rather than globbing
    

class ImageReorderApp(QListWidget):
    def __init__(self, image_paths):
        super().__init__()

        #loads order file if it exists, otherwise creates a new one
        order_file = os.path.join(dst_dir, 'order.txt')
        imgorder = []

        if os.path.exists(order_file):
            print(f"Loading existing order from {order_file}")
            with open(order_file, 'r') as f:
                imgorder = [line.strip() for line in f if line.strip()]
        else:
            # create empty file
            print(f"Creating new order file at {order_file}")
            with open(order_file, 'w') as f:
                pass
        
        self.setDragDropMode(QListWidget.InternalMove)  # enable drag and drop reorder
        self.setIconSize(QSize(100, 100))  # set icon size to image size

        #if the image is not in the order file, add it to the end of the list
        for path in webp_images:
            if path not in imgorder:
                imgorder.append(path)

        for img in imgorder:
            item = QListWidgetItem(QIcon(img), "")  # empty text, just icon
            item.setData(Qt.UserRole, img)
            self.addItem(item)
    
    def getNewOrder(self):
        paths = []
        for i in range(self.count()):
            item = self.item(i)
            if item:
                paths.append(item.data(Qt.UserRole))

        # write the new order to order.txt
        print("Saving new order to order.txt")
        with open(os.path.join(dst_dir, 'order.txt'), 'w') as f:
            for path in paths:
                f.write(path + '\n')
        
        os.system(f'python3 "{os.path.join(src_dir, "siteupdater.py")}"')


if __name__ == '__main__':
    print (webp_images)
    app = QApplication(sys.argv)
    image_paths = webp_images
    window = ImageReorderApp(image_paths)
    window.setWindowTitle("Drag to Reorder Images")
    window.resize(300, 600)
    window.show()

    app.aboutToQuit.connect(window.getNewOrder)

    sys.exit(app.exec_())
