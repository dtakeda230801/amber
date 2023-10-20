
class cInputGateway:

	opt1 = False
	opt2 = False
	opt3 = False

	def __init__(self,comGen):
		self.commandGenerator = comGen

	def setPressEvent(self, ev,word):
		if ev.startswith('Control'):
			self.opt1 = True	
		elif ev.startswith('Shift'):
			self.opt2 = True	
		elif ev.startswith('Alt'):
			self.opt3 = True
		elif ev.startswith('F'):
			self._dispatchFunction(ev)
		elif ev.startswith('Left') or ev.startswith('Right') or ev.startswith('Up') or ev.startswith('Down'):
			self._dispatchCursor(ev)
		elif ev.startswith('Delete'):
			self.commandGenerator.setDelete()	
		elif ev.startswith('Escape'):
			self.commandGenerator.setEscape()
		elif ev.startswith('BackSpace'):
			self.commandGenerator.setBackSpace()
		elif ev.startswith('Return'):
			self.commandGenerator.setReturn()
		else:
			self._dispatchText(word)
 
	def setReleaseEvent(self, ev):
		if ev.startswith('Control'):
			self.opt1 = False	
		elif ev.startswith('Shift'):
			self.opt2 = False	
		elif ev.startswith('Alt'):
			self.opt3 = False
	
	def _dispatchCursor(self, direction):
		self.commandGenerator.setCursor(direction,self.opt1,self.opt2,self.opt3)

	def _dispatchFunction(self, function):
		self.commandGenerator.setFunction(function)

	def _dispatchText(self, text):
		self.commandGenerator.setText(text)

