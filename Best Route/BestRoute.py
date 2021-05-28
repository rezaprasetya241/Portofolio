import math
import pygame
from queue import PriorityQueue

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Find the best Route")
BG = (44, 62, 80)
GREY = (128,128,128)
class Node:
	def __init__(self,row,col,width,totalRows):
		self.row = row
		self.col = col
		self.width = width
		self.totalRows = totalRows
		self.x = row*width
		self.y = col*width
		self.color = BG
		self.neighbors = []

	def getPosition(self):
		return self.x, self.y
	def open(self):
		return self.color == (39, 174, 96)
	def makeOpen(self):
		self.color = (39, 174, 96)
	def close(self):
		return self.color == (44, 62, 80)
	def makeClose(self):
		self.color = (44, 62, 80)
	def forStart(self):
		return self.color == (255, 0, 0)
	def makeStart(self):
		self.color = (255, 0, 0)
	def forEnd(self):
		return self.color == (0, 120, 255)
	def makeEnd(self):
		self.color = (0, 120, 255)
	def forWall(self):
		return self.color == (0,0,0)
	def makeWall(self):
		self.color = (0, 0, 0)
	def makePath(self):
		self.color = (255, 255, 0)
	def reset(self):
		self.color = BG
	def show(self, win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
	


	def getNeighbors(self,grid):
		if self.col < self.totalRows-1 and not grid[self.row][self.col+1].forWall():
			self.neighbors.append(grid[self.row][self.col+1])
		if self.col > 0 and not grid[self.row][self.col-1].forWall():
			self.neighbors.append(grid[self.row][self.col-1])

		if self.row < self.totalRows-1 and not grid[self.row+1][self.col].forWall():
			self.neighbors.append(grid[self.row+1][self.col])
		if self.row > 0 and not grid[self.row-1][self.col].forWall():
			self.neighbors.append(grid[self.row-1][self.col])

# draw for the best route
def bestRoute(cameFrom,current,show):
	while current in cameFrom:
		current = cameFrom[current]
		current.makePath()
		show()
def heuristic(i1,i2):
	x1,y1 = i1
	x2,y2 = i2
	return abs(x2-x1)+abs(y2-y1)

#algorithm
def findBestRoute(draw, grid, start, end):
	count = 0
	setOpen = PriorityQueue()
	setOpen.put((0, count, start))
	came_from = {}
	prevScore = {node: float("inf") for row in grid for node in row}
	prevScore[start] = 0
	nextScore = {node: float("inf") for row in grid for node in row}
	nextScore[start] = heuristic(start.getPosition(), end.getPosition())

	setOpenHash = {start}

	while setOpen.empty()==False: #while open_set is full
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = setOpen.get()[2]
		setOpenHash.remove(current)

		if current == end:
			bestRoute(came_from, end, draw)
			start.makeStart()
			end.makeEnd()
			return True

		for neighbor in current.neighbors:
			tempPrevScore = prevScore[current] + 1

			if tempPrevScore < prevScore[neighbor]:
				came_from[neighbor] = current
				prevScore[neighbor] = tempPrevScore
				nextScore[neighbor] = tempPrevScore + heuristic(neighbor.getPosition(), end.getPosition())
				if neighbor not in setOpenHash:
					count += 1
					setOpen.put((nextScore[neighbor], count, neighbor))
					setOpenHash.add(neighbor)
					neighbor.makeOpen()

		draw()
	return False

#action when click map for get cordinate
def getClick(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap
	return row, col

#build map	
def buildMap(row, width):
	grid = []
	lines = width // row
	for i in range(row):
		grid.append([])
		for j in range(row):
			node = Node(i, j, lines, row)
			grid[i].append(node)
	return grid

#build border
def drawGrid(win, row, width):
	lines = width // row
	for x in range(row):
		pygame.draw.line(win, GREY, (0, x*lines), (width, x*lines))
		for i in range(row):
			pygame.draw.line(win, GREY, (i *lines, 0), (i*lines, width))

#for display
def draw(win, grid, row, width):
	for rows in grid:
		for node in rows:
			node.show(win)
	drawGrid(win, row, width)
	pygame.display.update()

def main(win, width):
	lines = 50
	grid = buildMap(lines, width)

	start = None
	goals = None
	while True:
		draw(win, grid, lines, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			if pygame.mouse.get_pressed()[0]: # LEFT
				position = pygame.mouse.get_pos()
				row, col = getClick(position, lines, width)
				node = grid[row][col]
				if not start and node != goals:
					start = node
					start.makeStart()

				elif not goals and node != start:
					goals = node
					goals.makeEnd()

				elif node != goals and node != start:
					node.makeWall()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				position = pygame.mouse.get_pos()
				row, col = getClick(position, lines, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				if node == goals:
					goals = None

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN and start and goals:
					for row in grid:
						for node in row:
							node.getNeighbors(grid)
							

					findBestRoute(lambda: draw(win, grid, lines, width), grid, start, goals)

				#for clear screen
				if event.key == pygame.K_c:
					start = None
					goals = None
					grid = buildMap(lines, width)
	pygame.quit()

main(WIN, WIDTH)