import unreal
import sys
import os
import qdarkstyle
from PySide2 import QtGui,QtCore,QtWidgets
from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt, QSize
from unreal import StaticMesh as mesh
from unreal import Vector

#TODO: Get selection from CB
#TODO: Split them up on classes
#TODO: Spawn actors in level with offset based on BBox (or maybe Collision bounds)

#TODO: Figure out how calculating bboxes works
#TODO: Figure out how to move the next prop based on the previous prop Bbox
#TODO: Expose options for display
    #TODO: Text Labels, Row, and Columns
    #TODO: Padding

"""
APi docs
https://docs.unrealengine.com/4.27/en-US/PythonAPI/search.html?q=bounding+box
"""

 

unreal.log("---Starting the show---")

# Variables

Author = "Ioan-Andrei Nistor"
Contact = "ioan.andrei.nistor@gmail.com"
StyleSheetFile = "D:/GitHubRepos/UnrealMapPopulator/UnrealMapPop/darkOrange.css"

class TestWidget(QtWidgets.QWidget):
    loop_count = 0
    coord_x = 0
    coord_y = 0
    coord_z = 250

    def __init__(self, parent=None):

        super(TestWidget, self).__init__(parent)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Level Populator")
        self.setMinimumSize(200,100)
        self.setWindowOpacity(0.9)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        print (dir_path)

        with open(StyleSheetFile, "r") as sh:
            self.setStyleSheet(sh.read())

        vbox = QtWidgets.QVBoxLayout(self)
        btn = QtWidgets.QPushButton('Populate Level')
        btn.clicked.connect(self.btn_clicked)        
        vbox.addWidget(btn)

        label_row = QtWidgets.QLabel()
        label_row.setText(("Rows"))
        vbox.addWidget(label_row)
        row_spin = QtWidgets.QSpinBox()
        row_spin.setMinimum(1)
        vbox.addWidget(row_spin)

        label_column = QtWidgets.QLabel()
        label_column.setText(("Columns"))
        vbox.addWidget(label_column)
        column_spin = QtWidgets.QSpinBox()
        column_spin.setMinimum(1)
        vbox.addWidget(column_spin)
        
        btn_quit = QtWidgets.QPushButton('Quit')
        btn_quit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        vbox.addWidget(btn_quit)




    
    def pop_message_window(self, title, description): # Self so it does not cry <3

        unreal.EditorDialog.show_message(title, description,message_type=unreal.AppMsgType.OK)
        
    def populate_level(self):

        # Still Need to Fix a proper offset between assets
        self.assets = unreal.EditorUtilityLibrary.get_selected_assets() 
        if len(self.assets) == 0:
            unreal.EditorDialog.show_message("Wold Populator", "Error: Please select Static Meshes from Content Browser!",message_type=unreal.AppMsgType.OK)
        else:      
            for i in self.assets:
                asset_data = unreal.EditorUtilityLibrary.get_selected_asset_data()
                asset_path = unreal.EditorUtilityLibrary.get_path_name(self.assets[self.loop_count])       # Getting the path to the selected asset
                try_to_load = unreal.EditorAssetLibrary.load_asset(asset_path)
                unreal.log("---Calculating BBox Location Offsets---")
                self.get_bbox_min = mesh.get_bounding_box(i).min.x
                self.get_bbox_max = mesh.get_bounding_box(i).max.x 
                self.coord_x = self.coord_x - self.get_bbox_min *2.5
                actor_location_math = unreal.Vector(self.coord_x, self.coord_y, self.coord_z)
                print (actor_location_math.x, actor_location_math.y, actor_location_math.z)
                actor_rotation = unreal.Rotator(0.0, 0.0, 0.0)      # Dont really think this will ever be needed but its here in case its needed
                unreal.EditorLevelLibrary.spawn_actor_from_object(try_to_load, actor_location_math, actor_rotation)
                self.loop_count += 1 
        return self.loop_count

    def get_number_of_assets(self):
        self.total_assets_places = str(str("Total of: ") + str(self.loop_count) + str(" assets placed"))
        # self.pop_message_window("LevelPopulator", self.total_assets_places)

    def btn_clicked(self):
        print('Clicked')
        unreal.log('---Clicked---')
        self.populate_level()
        self.get_number_of_assets()
        self.loop_count = 0 # Reseting Counter in case you want to place it again

    def quit_app(self):
        app.quit()



unreal.log("---Curtain Drop---")

app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()


# app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

widget = TestWidget()
widget.show()
unreal.parent_external_window_to_slate(widget.winId())