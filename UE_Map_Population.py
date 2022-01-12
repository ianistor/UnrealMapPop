from typing import Text
import PySide2
import unreal
import sys
import os
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt, QSize
from unreal import HorizontalAlignment, StaticMesh as mesh
from unreal import Vector

#TODO: Add different classes errors/solutions
#TODO: Add a folder in the Level called Assets
#TODO: Work on Row/Column functionality
#TODO: Figured out why two text labels are getting spawned
#TODO: Figure out how to cleanly modify last added prop value from level (To modify Text name)
#TODO: Add Object name on the Text Label


"""
APi docs
https://docs.unrealengine.com/4.27/en-US/PythonAPI/search.html?q=bounding+box
"""

 

unreal.log("---Starting the show---")

"""
Author = "Ioan-Andrei Nistor"
Contact = "ioan.andrei.nistor@gmail.com"
"""



StyleSheetFile = "D:/GitHubRepos/UnrealMapPopulator/UnrealMapPop/darkOrange.css"


class TestWidget(QtWidgets.QWidget):
    loop_count = 0
    coord_y = 0
    coord_x = 0
    coord_z = 250
    current_bbox_x = 0
    record_maxbbox_x = 0

    #For Progress Bar if needed later
    total_frames = 100
    text_label_progress = "Placing your assets..."



    def __init__(self, parent=None):

        super(TestWidget, self).__init__(parent)
    
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
            )
        # self.setWindowFlag(Qt.FramelessWindowHint) # This makes its headerless (looks nicer)
        self.setWindowTitle("Level Populator")
        self.setMinimumSize(200,100)
        self.setWindowOpacity(0.9)
        self.offset = None


        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # print (dir_path)

        with open(StyleSheetFile, "r") as sh:
            self.setStyleSheet(sh.read())

        vbox = QtWidgets.QVBoxLayout(self)
        btn = QtWidgets.QPushButton('Populate Level')
        btn.clicked.connect(self.btn_populate)        
        vbox.addWidget(btn)

        btn_test = QtWidgets.QPushButton("Test Button")
        btn_test.clicked.connect(self.btn_test)
        vbox.addWidget(btn_test)

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
        # btn_quit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn_quit.clicked.connect(self.quit_app)
        vbox.addWidget(btn_quit)


# # # UI WORK FOR MOUSE DRAG AND DROP
#     def mousePressEvent(self, event):
#         if event.button() == QtCore.Qt.LeftButton:
#             self.offset = event.pos()
#         else:
#             super().mousePressEvent(event)

#     def mouseMoveEvent(self, event):
#         if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
#             self.move(self.pos() + event.pos() - self.offset)
#         else:
#             super().mouseMoveEvent(event)

#     def mouseReleaseEvent(self, event):
#         self.offset = None
#         super().mouseReleaseEvent(event)

    
    def pop_message_window(self, title, description): # Self so it does not cry <3
        """Poping a message window

        Args:
            title ([type]): [description]
            description ([type]): [description]
        """
        unreal.EditorDialog.show_message(title, description,message_type=unreal.AppMsgType.OK)

    def get_class(self, asset):
        # get the class instance and the clear text name
        print ("Looking into Class of Selected")
        self.editor_util = unreal.EditorUtilityLibrary()
        self.selected_assets = self.editor_util.get_selected_assets()
        for i in self.selected_assets:
            self.asset_name = asset.get_fname()
            self.asset_class = asset.get_class()
            self.class_name = system_lib.get_class_display_name(self.asset_class)


    def create_level_folder(self):
        # Lets create a folder to place assets in
        # unreal.EditorLevelUtils.get_name()
        return

    def create_text_render(self, placing):
        """
        Adds a text render asset to the level in front of the last added asset.
        Expects placing location args
        """
        # Spawn Asset
        unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.TextRenderActor, unreal.Vector(placing), unreal.Rotator(0,0,0))
        # Do math to figure out max bbox of last placed prop to figure out placement of the text label, i need to decide if i want it below the prop (which would make sense) or on top
        print (unreal.PropertyValue.set_editor_property(Text, "PleaseWork!"))  # This does not work for some reason, maybe i need to get selection of last placed asset before?


    def populate_level(self):
        self.assets = unreal.EditorUtilityLibrary.get_selected_assets() 
        if len(self.assets) == 0:
            unreal.EditorDialog.show_message("Wold Populator", "Error: Please select Static Meshes from Content Browser!",message_type=unreal.AppMsgType.OK)
        else:      
            with unreal.ScopedEditorTransaction("Undo Stack") as trans:   #Undo Stack
                for i in self.assets:
                    asset_data = unreal.EditorUtilityLibrary.get_selected_asset_data()
                    # asset_type = unreal.EditorUtilityLibrary.get_class()
                    # print (asset_type)
                    asset_path = unreal.EditorUtilityLibrary.get_path_name(self.assets[self.loop_count])       # Getting the path to the selected asset
                    try_to_load = unreal.EditorAssetLibrary.load_asset(asset_path)
                
                    unreal.log("---Calculating BBox Location Offsets---")
                    self.get_bbox_min = mesh.get_bounding_box(i).min.y
                    self.get_bbox_max = mesh.get_bounding_box(i).max.y
                    self.current_bbox_x = mesh.get_bounding_box(i).max.x
                    if self.current_bbox_x > self.record_maxbbox_x:
                        self.record_maxbbox_x = self.current_bbox_x
                        print ("---Found bigger mesh, recording max size for offset---")
                    self.coord_y = self.coord_y - self.get_bbox_min *2.5 + self.get_bbox_max # Not sure if i really need to + the bbox_max 
                    actor_location_math = unreal.Vector(self.coord_x, self.coord_y, self.coord_z)
                    print (actor_location_math.x, actor_location_math.y, actor_location_math.z)
                    actor_rotation = unreal.Rotator(0.0, 0.0, 0.0)      # Dont really think this will ever be needed but its here in case its needed
                    unreal.EditorLevelLibrary.spawn_actor_from_object(try_to_load, actor_location_math, actor_rotation)
                    # self.create_text_render(actor_location_math) #REPLACE ACTOR_LOCATION_MATH WITH PROPER LOCATION 
                    self.loop_count += 1 
                    self.coord_y = self.coord_y - self.get_bbox_min *2 # Keep offsetting
                    
                    # Ge
                    # t highest number of BBox on X from previous placement
                
        return self.loop_count

    def get_number_of_assets(self):
        self.total_assets_places = str(str("Total of: ") + str(self.loop_count) + str(" assets placed"))
        # self.pop_message_window("LevelPopulator", self.total_assets_places)

    def select_last_placed_asset(self):
        #TODO: Create a function that returns as selection the last placed asset
        return

    def btn_populate(self):
        self.populate_level()
        self.get_number_of_assets()
        self.loop_count = 0 # Reseting Counter in case you want to place it again
    
    def btn_test(self):
        self.create_text_render()

    def quit_app(self):
        unreal.log("---Quitting---")
        self.close()


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