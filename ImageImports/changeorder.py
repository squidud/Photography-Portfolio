from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtCore import Qt, QMimeData
import sys
import os
import glob

src_dir = os.path.dirname(os.path.abspath(__file__))
dst_dir = os.path.abspath(os.path.join(src_dir, '../Images'))
webp_images = glob.glob(os.path.join(dst_dir, '*.webp'))
ordered_images = []

# Gallery order from HTML
gallery_order = [
    'DSC02610.webp', 'IMG_3923.webp', 'IMG_8670.webp', 'IMG_8692.webp', 'IMG_3958.webp',
    '20230702112603_IMG_8136.webp', 'DSC00130.webp', 'DSC00286.webp', 'PICT0379.webp',
    '20240725231033_IMG_3792.webp', 'IMG_3811.webp', '20230316192237_IMG_7304.webp',
    'IMG_8657.webp', '20240325023951_IMG_2827.webp', 'DSC01957.webp', 'DSC00081.webp',
    '20240725230736_IMG_3790 (1).webp', 'PICT0421.webp', '20240611091105_IMG_3544.webp',
    'DSC02527.webp', 'DSC00131.webp', 'IMG_8694.webp', 'DSC00170.webp', 'DSC00205.webp',
    '20240625023451_IMG_3616.webp', 'IMG_8758.webp', '20240601005934_IMG_3522.webp',
    'DSC03111.webp', 'IMG_8781.webp', 'IMG_8847.webp', 'DSC01056 (1).webp', 'IMG_8685.webp',
    'Cologne-Photo.webp', 'PICT0017.webp', 'PICT0410.webp', '20240725044139_IMG_3778.webp',
    'DSC02074.webp', 'PICT0411.webp', '20240721_155643.webp', '20240329004932_IMG_3091.webp',
    '20240521055946_IMG_3413.webp', '20230305141617_IMG_7254.webp', '000267280022.webp',
    '20240326052340_IMG_2949.webp', 'DSC00156.webp', 'L16_00035.webp', '000267270016.webp',
    'DSC00552.webp', 'DSC01085.webp', 'IMG_3946.webp', '20230503170955_IMG_7703.webp',
    'IMG_8824.webp', 'PICT0388.webp', '20240625023635_IMG_3621.webp', '20240521005714_IMG_3388.webp',
    'PICT0404.webp', '000267270023.webp', '20240325025008_IMG_2840.webp', 'IMG_8613.webp',
    'PICT0394.webp', 'IMG_3376.webp', 'L16_00017.webp', 'IMG_8852.webp',
    'ReLens-ReLens_Image__2023-05-25_15_38_143000x4000 (1).webp', 'DSC01905.webp',
    'IMG_8845.webp', '20240625022956_IMG_3610.webp', 'DSC02558.webp', 'DSC01934.webp',
    '20240324100130_IMG_2739.webp', 'DSC02621.webp', 'DSC02702-2.webp', 'IMG_3937.webp',
    'PICT0398.webp', 'IMG_3813.webp', 'DSC00539.webp', 'DSC01693.webp', 'DSC01943.webp',
    'AurielSmoking.webp', '20240724031806_IMG_3721 (1).webp', '20240324102412_IMG_2788.webp',
    '20230711204300_IMG_8196.webp', 'DSC01885.webp', 'IMG_4011.webp', '20240625022818_IMG_3606.webp',
    'IMG_3936.webp', 'IMG_3920.webp', 'PICT0365 (1).webp', 'DSC03091.webp', 'DSC03132.webp'
]    

class DraggableLabel(QLabel):
    def __init__(self, image_path, index, parent_widget):
        super().__init__()
        self.image_path = image_path
        self.index = index
        self.parent_widget = parent_widget
        self.is_dragging = False
        
        # Load and scale image
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px solid #666; margin: 2px; background: white;")
        self.setMinimumSize(154, 154)  # Account for border and margin
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.setStyleSheet("border: 2px solid #0078d4; margin: 2px; background: #e6f3ff;")
            
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if ((event.pos() - self.drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
            
        if not self.is_dragging:
            self.is_dragging = True
            drag = QDrag(self)
            mimeData = QMimeData()
            mimeData.setText(str(self.index))
            drag.setMimeData(mimeData)
            
            # Create pixmap for drag
            drag_pixmap = self.pixmap().scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            drag.setPixmap(drag_pixmap)
            drag.setHotSpot(drag_pixmap.rect().center())
            
            # Execute drag
            drag.exec_(Qt.MoveAction)
            self.is_dragging = False
            self.setStyleSheet("border: 2px solid #666; margin: 2px; background: white;")
            
    def mouseReleaseEvent(self, event):
        self.setStyleSheet("border: 2px solid #666; margin: 2px; background: white;")

class ImageReorderApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.image_labels = []
        self.current_order = []
        
        # Load existing order or use gallery order
        order_file = os.path.join(dst_dir, 'order.txt')
        if os.path.exists(order_file):
            print(f"Loading existing order from {order_file}")
            with open(order_file, 'r') as f:
                file_order = [line.strip() for line in f if line.strip()]
            # Convert full paths to just filenames for comparison
            self.current_order = file_order
        else:
            print(f"Using gallery order")
            # Use gallery order, converting to full paths
            self.current_order = []
            for filename in gallery_order:
                full_path = os.path.join(dst_dir, filename)
                if os.path.exists(full_path):
                    self.current_order.append(full_path)
            
        # Add any missing images to the end
        existing_filenames = [os.path.basename(path) for path in self.current_order]
        for path in webp_images:
            filename = os.path.basename(path)
            if filename not in existing_filenames:
                self.current_order.append(path)
        
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Create scroll area
        scroll = QScrollArea()
        scroll_widget = QWidget()
        
        # Create grid layout for images
        self.grid_layout = QGridLayout(scroll_widget)
        self.grid_layout.setSpacing(5)
        
        # Add images to grid (3 columns)
        for i, image_path in enumerate(self.current_order):
            if os.path.exists(image_path):
                label = DraggableLabel(image_path, i, self)
                self.image_labels.append(label)
                row = i // 3
                col = i % 3
                self.grid_layout.addWidget(label, row, col)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasText():
            source_index = int(event.mimeData().text())
            
            # Find which widget was dropped on
            drop_widget = self.childAt(event.pos())
            target_index = -1
            
            # Find target index
            for i, label in enumerate(self.image_labels):
                if label == drop_widget or drop_widget in [label] or self.isAncestorOf(label, drop_widget):
                    target_index = i
                    break
                    
            if target_index >= 0 and target_index != source_index:
                # Reorder the lists
                item = self.current_order.pop(source_index)
                self.current_order.insert(target_index, item)
                
                # Update indices
                for i, label in enumerate(self.image_labels):
                    label.index = i
                
                # Rebuild the grid
                self.rebuildGrid()
                
            event.accept()
        else:
            event.ignore()
            
    def isAncestorOf(self, ancestor, child):
        """Check if ancestor widget contains child widget"""
        parent = child.parent() if hasattr(child, 'parent') else None
        while parent:
            if parent == ancestor:
                return True
            parent = parent.parent() if hasattr(parent, 'parent') else None
        return False
        
    def rebuildGrid(self):
        """Rebuild the grid layout with current order"""
        # Clear existing layout
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
            
        # Re-add widgets in new order
        self.image_labels.clear()
        for i, image_path in enumerate(self.current_order):
            if os.path.exists(image_path):
                label = DraggableLabel(image_path, i, self)
                self.image_labels.append(label)
                row = i // 3
                col = i % 3
                self.grid_layout.addWidget(label, row, col)
    
    def getNewOrder(self):
        # Save current order
        paths = self.current_order
        
        # write the new order to order.txt
        print("Saving new order to order.txt")
        print(f"New order has {len(paths)} images")
        with open(os.path.join(dst_dir, 'order.txt'), 'w') as f:
            for path in paths:
                f.write(path + '\n')
        
        print("Running siteupdater.py...")
        os.system(f'python3 "{os.path.join(src_dir, "siteupdater.py")}"')


if __name__ == '__main__':
    print (webp_images)
    app = QApplication(sys.argv)
    window = ImageReorderApp()
    window.setWindowTitle("Drag to Reorder Images")
    window.resize(800, 600)
    window.show()

    app.aboutToQuit.connect(window.getNewOrder)

    sys.exit(app.exec_())
