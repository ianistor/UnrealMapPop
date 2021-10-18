import unreal
import sys
import qdarkstyle
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2.QtGui import QPalette, QColor
from unreal import StaticMesh as mesh
from unreal import Vector

#TODO: Get selection from CB
#TODO: Split them up on classes
#TODO: Spawn actors in level with offset based on BBox (or maybe Collision bounds)

#TODO: Figure out how calculating bboxes works
#TODO: Figure out how to move the next prop based on the previous prop Bbox

"""
APi docs
https://docs.unrealengine.com/4.27/en-US/PythonAPI/search.html?q=bounding+box
"""

# Global Variables 

unreal.log("---Starting the show---")

loop_count = 0
coord_x = 0
coord_y = 0
coord_z = 250

class TestWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):

        super(TestWidget, self).__init__(parent)

        vbox = QtWidgets.QVBoxLayout(self)
        btn = QtWidgets.QPushButton('Test')
        btn.clicked.connect(self.btn_clicked)
        vbox.addWidget(btn)



        
    def populate_level(self):

        assets = unreal.EditorUtilityLibrary.get_selected_assets() 

        if len(assets) == 0:
            unreal.EditorDialog.show_message("Wold Populator", "Error: Please select Static Meshes from Content Browser!",message_type=unreal.AppMsgType.OK)
        else:      
            for i in assets:
                asset_data = unreal.EditorUtilityLibrary.get_selected_asset_data()
                asset_path = unreal.EditorUtilityLibrary.get_path_name(assets[loop_count])       # Getting the path to the selected asset
                try_to_load = unreal.EditorAssetLibrary.load_asset(asset_path)
                unreal.log("---Calculating BBox Location Offsets---")
                get_bbox_min = mesh.get_bounding_box(i).min.x
        
                get_bbox_max = mesh.get_bounding_box(i).max.x 

                coord_x = coord_x - get_bbox_min *2.5
                actor_location_math = unreal.Vector(coord_x, coord_y, coord_z)
                print (actor_location_math)
                actor_rotation = unreal.Rotator(0.0, 0.0, 0.0)      # Dont really think this will ever be needed but its here in case its needed
                unreal.EditorLevelLibrary.spawn_actor_from_object(try_to_load, actor_location_math, actor_rotation)
                iteration += 1 
                # print ('Asset' , (asset_path) , 'placed at location ' , (actor_location))
                # unreal.EditorDialog.show_message("Wold Populator", "Your assets have been placed in your level",message_type=unreal.AppMsgType.OK)

    def btn_clicked(self):
        print('Clicked')

        unreal.log('---Clicked---')
        self.populate_level()

    def do_something():

        # lets move stuff in functions
        return


unreal.log("---Curtain Drop---")

app = None
if not QtWidgets.QApplication.instance():
	app = QtWidgets.QApplication(sys.argv)


# app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

widget = TestWidget()
widget.show()
unreal.parent_external_window_to_slate(widget.winId())