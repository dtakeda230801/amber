from ObjectManager import *

class cUIOrganizer:

    drawCursorCallbacks         = []
    drawColorIndicatorCallbacks = []
    cursorType                  = 'normal'
    colorIndex                  = 0
    colorTable                  = ['Black','Blue','Red','Green']


    def __init__(self,objectManager):
        self.object_manager = objectManager
        self.object_manager.setRequestCurrentLocationCallback(self._requestCurrentLocation)
        self.object_manager.setModeChangeCallback(self._onModeChange)

    def configure(self,canvas_w,canvas_h,cursor_w,cursor_h,drawCursorCallback,drawColorIndicatorCallback):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.cursor_w = cursor_w
        self.cursor_h = cursor_h
        self.drawCursorCallbacks.append(drawCursorCallback)
        self.drawColorIndicatorCallbacks.append(drawColorIndicatorCallback)

        self.x_margin = int(self.cursor_w/2)
        self.y_margin = int(self.cursor_h/2)

        self.cursor_x = self.x_margin
        self.cursor_y = self.y_margin

        self._updateCursor()
        self._udpateColor()

    def moveCursor(self,deltaX,deltaY,hold):

        tag = None

        if hold:
            tag = self.object_manager.checkHit(self.cursor_x,self.cursor_y)

        self.cursor_x = self.cursor_x + deltaX
        self.cursor_y = self.cursor_y + deltaY

        if self.cursor_x < self.x_margin:
            self.cursor_x = self.x_margin

        if self.cursor_x > self.canvas_w - self.x_margin:
            self.cursor_x = self.canvas_w - self.x_margin

        if self.cursor_y < self.y_margin:
            self.cursor_y = self.y_margin

        if self.cursor_y > self.canvas_h - self.y_margin:
            self.cursor_y = self.canvas_h - self.y_margin

        if tag != None:
            self.object_manager.moveObject(tag)

        self._updateCursor()

    def changeColor(self):
        self.colorIndex = self.colorIndex + 1
        if self.colorIndex == len(self.colorTable):
            self.colorIndex = 0
        self._udpateColor()

    def _updateCursor(self):
        self._checkHit()
        for drawCursorCallback in self.drawCursorCallbacks:
            drawCursorCallback('cursor',self.cursor_x,self.cursor_y,self.cursorType)

    def _udpateColor(self):
        self.object_manager.setColor(self.colorTable[self.colorIndex])
        for drawColorIndicatorCallback in self.drawColorIndicatorCallbacks:
            drawColorIndicatorCallback('color', self.canvas_w - 30, 10,15,15, self.colorTable[self.colorIndex])
                                       
    def _requestCurrentLocation(self):
        return (self.cursor_x,self.cursor_y)
    
    def _onModeChange(self):
        if self.object_manager.isEditingText() or self.object_manager.isEditingFigure() or self.object_manager.isEditingFreeline():
            self.cursorType = 'editing'
        else:
            self.cursorType = 'normal'

        self._updateCursor()

    def _checkHit(self):
        hitTag = self.object_manager.checkHit(self.cursor_x,self.cursor_y)
        if self.cursorType == 'normal' and hitTag != None:
            self.cursorType = 'selecting'
        elif self.cursorType == 'selecting' and hitTag == None:
            self.cursorType = 'normal'
        


            

