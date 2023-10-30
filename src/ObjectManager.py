import uuid
import math

class cObject:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.tag = ''
        self.w = 0
        self.h = 0
        self.objType = ''
        self.color =''
        self.text = []
        self.points = []

class cObjectManager:

    state        = 'ready'
    objs         = []
    currentObj   = None

    def setRequestCurrentLocationCallback(self,cb):
        self.request_current_location = cb

    def setModeChangeCallback(self,cb):
        self.on_mode_change = cb

    def setObjectDrawCallback(self,cb):
        self.on_object_draw = cb

    def setColor(self,color):
        self.color = color

    def checkHit(self,x,y):
        for obj in self.objs:
            left   = obj.x
            top    = obj.y
            right  = obj.x + obj.w
            buttom = obj.y + obj.h

            if left <= x and top <= y and x <= right and y <= buttom:
                return obj.tag
        
        return None

    def handleText(self,text):
        if self.state == 'ready':
            self.state              = 'text'
            self.currentObj         = cObject()
            self.currentObj.objType = 'text'
            self.currentObj.color   = self.color
            self.currentObj.tag     = self._makeTag()
            self.currentObj.w       = 50
            self.currentObj.h       = 20
            self.points             = []
            (self.currentObj.x, self.currentObj.y) = self.request_current_location()

            self.on_mode_change()

        elif self.state != 'text':
            return

        self.currentObj.text.append(text)
        self._update()

    def handleBackSpace(self):
        if self.state != 'text':
            return
        if len(self.currentObj.text)> 0:
            del self.currentObj.text[len(self.currentObj.text) - 1]
            self._update()

    def handleReturn(self):
        if self.state != 'text':
            return
        self.currentObj.text.append('\n')
        self._update()

    def createFigure(self,objType):
        if self.state == 'ready':
            if objType == 'freeline' or objType == 'freearrow':
                self.state      = 'freeline'
            else:
                self.state      = 'figure'

            self.currentObj         = cObject()
            self.currentObj.objType = objType
            self.currentObj.color   = self.color
            self.currentObj.tag     = self._makeTag()
            self.currentObj.w       = 0
            self.currentObj.h       = 0
            (self.currentObj.x, self.currentObj.y) = self.request_current_location()

            if objType == 'curve' or objType == 'triangle' or objType == 'freeline' or objType == 'freearrow':
                self.currentObj.points = [(self.currentObj.x, self.currentObj.y),(self.currentObj.x, self.currentObj.y)]
            else:
                self.points = []
            self.on_mode_change()
            self._update()

    def updateFigure(self):
        (x, y) = self.request_current_location()

        if self.currentObj.objType == 'curve':
            if x - self.currentObj.x == 0:
                delta = 0
            else:
                delta = abs(y - self.currentObj.y) / abs(x - self.currentObj.x)
            if delta > 1.0:
                self.currentObj.points = [(self.currentObj.x, self.currentObj.y),(self.currentObj.x,y),(x,y)]
            else:
                self.currentObj.points = [(self.currentObj.x, self.currentObj.y),(x,self.currentObj.y),(x,y)]
            self.currentObj.w = x - self.currentObj.x
            self.currentObj.h = y - self.currentObj.y

        elif self.currentObj.objType == 'triangle':
            x1 = int(math.cos(math.radians(30))*(x - self.currentObj.x) - math.sin(math.radians(30))*(y-self.currentObj.y) ) + self.currentObj.x
            y1 = int(math.sin(math.radians(30))*(x - self.currentObj.x) + math.cos(math.radians(30))*(y-self.currentObj.y) ) + self.currentObj.y

            x2 = int(math.cos(math.radians(-30))*(x - self.currentObj.x) - math.sin(math.radians(-30))*(y-self.currentObj.y) ) + self.currentObj.x
            y2 = int(math.sin(math.radians(-30))*(x - self.currentObj.x) + math.cos(math.radians(-30))*(y-self.currentObj.y) ) + self.currentObj.y

            self.currentObj.points = [(self.currentObj.x, self.currentObj.y),(x1,y1),(x2,y2),(self.currentObj.x, self.currentObj.y)]

            minX = min([self.currentObj.x,x1,x2])
            maxX = max([self.currentObj.x,x1,x2])
            minY = min([self.currentObj.y,y1,y2])
            maxY = max([self.currentObj.y,y1,y2])

            self.currentObj.w = maxX - minX
            self.currentObj.h = maxY - minY

        elif self.currentObj.objType == 'freeline' or self.currentObj.objType == 'freearrow':
            pointNum = len(self.currentObj.points)
            self.currentObj.points[pointNum-1] = (x,y)

        else:
            self.currentObj.w = abs(x - self.currentObj.x)
            self.currentObj.h = abs(y - self.currentObj.y)
            self.currentObj.points = [(self.currentObj.x,self.currentObj.y),(x,y)]

        self._update()

    def commitText(self):
        print('commitText:',self.state)
        if self.state != 'text':
            return
        
        if len(self.currentObj.text) > 0:
            self.objs.insert(0,self.currentObj)
        
        self.state      = 'ready'
        self.currentObj = None
        self.on_mode_change()

    def commitFigure(self):
        if self.state != 'figure' and self.state != 'freeline':
            return
        
        minX = self.currentObj.x
        minY = self.currentObj.y
        maxX = self.currentObj.x
        maxY = self.currentObj.y
        for point in self.currentObj.points:
            if point[0] < minX:
                minX = point[0]

            if point[1] < minY:
                minY = point[1]

            if point[0] > maxX:
                maxX = point[0]

            if point[1] > maxY:
                maxY = point[1]

        self.currentObj.x = minX
        self.currentObj.y = minY

        self.currentObj.w = maxX - minX
        self.currentObj.h = maxY - minY

        if self.currentObj.w > 0 or self.currentObj.h > 0:
            self.objs.insert(0,self.currentObj)
        
        self.state      = 'ready'
        self.currentObj = None
        self.on_mode_change()

    def commitPoint(self):
        if self.state != 'freeline':
            return

        pointNum = len(self.currentObj.points)
        self.currentObj.points.append(self.currentObj.points[pointNum-1])
    
    def moveObject(self,tag):
        (x, y) = self.request_current_location()

        self.currentObj = self._findObjByTag(tag)

        deltaX = self.currentObj.x - x
        deltaY = self.currentObj.y - y
        
        self.currentObj.x = x
        self.currentObj.y = y

        newPoints = []
        for point in self.currentObj.points:
            newPoints.append((point[0] - deltaX,point[1] - deltaY))

        self.currentObj.points = newPoints

        self._update()
        self.currentObj = None

    def isEditingText(self):
        return (self.state == 'text')
    
    def isEditingFigure(self):
        return (self.state == 'figure')

    def isEditingFreeline(self):
        return (self.state == 'freeline')

    def delete(self):

        (x, y) = self.request_current_location()
        tag = self.checkHit(x, y)
        print(x,y,tag)
        if tag != None:
            self.objs.remove(self._findObjByTag(tag))
            self.on_object_draw(None,None,None,tag,None,None,None,None,None)
            self.on_mode_change()

    def _update(self):
        x       = self.currentObj.x
        y       = self.currentObj.y
        objType = self.currentObj.objType
        color   = self.color
        tag     = self.currentObj.tag
        w       = self.currentObj.w
        h       = self.currentObj.h
        text    = ''.join(self.currentObj.text)
        points  = self.currentObj.points

        self.on_object_draw(x,y,objType,tag,text,points,color)

    def _makeTag(self):
        tag = uuid.uuid4()
        return str(tag)

    def _findObjByTag(self,tag):
        for obj in self.objs:
            if obj.tag == tag:
                return obj

