from abc import ABC, abstractmethod

"""
This is supposed to be an abstract class the classes that inherit from it
have the logic to draw a game, for example the project for which I code this
MadPodRaceGraphic will have functions to draw a checkpoint, it will also
be able to draw players, indicating rotation etc
"""
class GameLogic(ABC):
	def __init__(self):
		pass

	"""
	This should be called after having instantiated The Graphical Game Engine
	so that pygame is initialised, then we can create fonts etc in the func
	"""
	@abstractmethod
	def init(self):
		pass

	@abstractmethod
	def processEvent(self, event):
		pass

	@abstractmethod
	def update(self, screen, data=None):
		pass