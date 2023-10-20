class cCommandGenerator:

    def __init__(self,uiOrganizer,objectManager):
        self.ui_organizer = uiOrganizer
        self.object_manager = objectManager

    def setCursor(self,direction,opt1,opt2,opt3):
        delta = 20
        if opt2:
            delta = 100
        elif opt3:
            delta = 5

        delta_x = 0
        delta_y = 0

        if direction == 'Left':
            delta_x = -1 * delta
        elif direction == 'Right':
            delta_x = delta
        elif direction == 'Down':
            delta_y = delta
        elif direction == 'Up':
            delta_y = -1 * delta

        self.ui_organizer.moveCursor(delta_x,delta_y,opt1)

        if self.object_manager.isEditingText():
           self.object_manager.commitText()
        elif self.object_manager.isEditingFigure() or self.object_manager.isEditingFreeline():
           self.object_manager.updateFigure()

    def setFunction(self,function):
        if self.object_manager.isEditingFigure():
            self.object_manager.commitFigure()
        else:
            if function == 'F1':
                self.object_manager.createFigure('line')
            elif function == 'F2':
                self.object_manager.createFigure('arrow')
            elif function == 'F3':
                self.object_manager.createFigure('curve')
            elif function == 'F4':
                self.object_manager.createFigure('rectangle')
            elif function == 'F5':
                self.object_manager.createFigure('triangle')
            elif function == 'F6':
                self.object_manager.createFigure('ellipse')
            elif function == 'F7':
                if self.object_manager.isEditingFreeline():
                    self.object_manager.commitPoint()
                else:
                    self.object_manager.createFigure('freeline')
            elif function == 'F8':
                if self.object_manager.isEditingFreeline():
                    self.object_manager.commitPoint()
                else:
                    self.object_manager.createFigure('freearrow')
            elif function == 'F12':
                self.ui_organizer.changeColor()

    def setText(self,text):
        self.object_manager.handleText(text)

    def setDelete(self):
        self.object_manager.delete()

    def setEscape(self):
        if self.object_manager.isEditingFigure():
            self.object_manager.commitFigure()
        elif self.object_manager.isEditingFreeline():
            self.object_manager.commitFigure()    

    def setBackSpace(self):
        self.object_manager.handleBackSpace()

    def setReturn(self):
        self.object_manager.handleReturn()



