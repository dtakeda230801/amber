from InputGateway import *
from CommandGenerator import *
from UIOrganizer import *
from ObjectManager import *

class cCore:
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(cCore, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.object_manager    = cObjectManager()
        self.ui_organizer      = cUIOrganizer(self.object_manager)
        self.command_generator = cCommandGenerator(self.ui_organizer,self.object_manager)
        self.input_gateway     = cInputGateway(self.command_generator)

    def configure(self,screen_w,screen_h,cursor_w,cursor_h,drawCursorCallback,drawColorIndicatorCallback,drawObjectCallback):
        self.ui_organizer.configure(screen_w,screen_h,cursor_w,cursor_h,drawCursorCallback,drawColorIndicatorCallback)
        self.object_manager.setObjectDrawCallback(drawObjectCallback)

    def setPressEvent(self,event,word):
        self.input_gateway.setPressEvent(event,word)

    def setReleaseEvent(self,event):
        self.input_gateway.setReleaseEvent(event)
