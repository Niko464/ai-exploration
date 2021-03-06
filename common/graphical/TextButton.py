import pygame

class TextButton():
	def __init__(self, x, y, text, font, drawBackground = False, color = "Black"):
		txtWidth, txtHeight = font.size(text)
		self.font = font
		self.color = color
		self.surface = font.render(text, False, color)
		self.x = x
		self.y = y
		self.rect = pygame.Rect(x, y, txtWidth, txtHeight)
		self.clicked = False
		self.drawBackground = drawBackground
		self.bgSurface = pygame.Surface((txtWidth, txtHeight))
		self.bgSurface.set_alpha(25)
		self.bgSurface.fill((20, 20, 20))

	def setText(self, newText):
		txtWidth, txtHeight = self.font.size(newText)
		self.surface = self.font.render(newText, False , self.color)
		self.rect = pygame.Rect(self.x, self.y, txtWidth, txtHeight)

	def update(self, screen, x: None, y: None):
		gotClicked = False
		mousePos = pygame.mouse.get_pos()

		if x is not None:
			self.rect.x = x
		if y is not None:
			self.rect.y = y
		#check mouseover and clicked conditions
		if self.rect.collidepoint(mousePos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				gotClicked = True
			elif self.clicked == True and pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

		#draw button on screen
		if (self.drawBackground):
			screen.blit(self.bgSurface, (self.rect.x, self.rect.y))
		screen.blit(self.surface, (self.rect.x, self.rect.y))
		return gotClicked