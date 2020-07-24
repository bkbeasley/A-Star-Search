import sys, pygame
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (29, 238, 17)
RED = (238, 17, 29)
PURPLE = (148, 17, 238)
WINDOW_WIDTH = 640
WINDOW_HEIGHT= 480
CELL_SIZE = 20

def main():
	global SCREEN, CLOCK

	""" Boolean value that is set to True once the user
	has selected a Start or End Node."""
	global START_NODE_SET, END_NODE_SET 

	global START_NODE, END_NODE

	# 2D-Array representing each cell of the grid as a Node object
	global MATRIX

	# Store the Nodes in the Open and Closed lists
	global OPEN_LIST, CLOSED_LIST

	global PATH_FOUND

	# Stores the x and y values of the Nodes in the shortest path
	global PATH_NODES_X, PATH_NODES_Y

	pygame.init()
	pygame.display.set_caption("A* Search")
	SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	CLOCK = pygame.time.Clock()

	START_NODE_SET = False
	START_NODE = {"x": None, "y": None, "f": None, "g": None, "h": None, "parent": None, "barrier": False}
	
	END_NODE = {"x": None, "y": None, "f": None, "g": None, "h": None, "parent": None, "barrier": False}
	END_NODE_SET = False

	OPEN_LIST = []
	CLOSED_LIST = []

	PATH_FOUND = False

	PATH_NODES_X = []
	PATH_NODES_Y = []

	SCREEN.fill(WHITE)

	drawCells()

	MATRIX = initCells()

	"""Used to prevent the application from calling
	findShortestPath() multiple times once the path has been found."""
	count = 0

	"""Used to prevent the application from calling
	drawShortestPath() multiple times.""" 
	foundCount = 0

	# Main application loop
	while True:
		events = pygame.event.get()

		if PATH_FOUND:
			if (foundCount < 1):
				drawShortestPath()
			foundCount += 1
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == 114:
						drawCells()
						pygame.display.update()
						foundCount = 0
						reset()

		for event in events:
			if event.type == pygame.KEYDOWN:
				# If space bar is pressed down
				if event.key == 32:
					if PATH_FOUND == False:
						findShortestPath()
					else:
						count += 1
						if count <= 1:
							drawShortestPath()
							count = 0

			# If the user clicks the left mouse button down
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					if START_NODE_SET == False or END_NODE_SET == False:
						drawStartEndNodes()
					else:
						if PATH_FOUND == False:
							drawBarrier()

			# Exit the application
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()


def reset():
	"""Resets lists and variables to empty, or falsy values"""
	global MATRIX
	global PATH_FOUND
	global OPEN_LIST, CLOSED_LIST
	global START_NODE, END_NODE
	global START_NODE_SET, END_NODE_SET
	global PATH_NODES_X, PATH_NODES_Y

	MATRIX = initCells()
	PATH_FOUND = False
	OPEN_LIST = []
	CLOSED_LIST = []
	START_NODE_SET = False
	START_NODE = {"x": None, "y": None, "f": None, "g": None, "h": None, "parent": None, "barrier": False}
	END_NODE = {"x": None, "y": None, "f": None, "g": None, "h": None, "parent": None, "barrier": False}
	END_NODE_SET = False
	PATH_NODES_X = []
	PATH_NODES_Y = []

def drawCells():
	"""Draws the cells of the grid.
	Scales with resolution sizes divisible by 20.
	"""
	column = 0
	row = 0
	for x in range(WINDOW_WIDTH):
		for y in range(WINDOW_HEIGHT):
			rect = pygame.Rect(column, row, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(SCREEN, WHITE, rect)
			pygame.draw.rect(SCREEN, BLACK, rect, 1)
			row += CELL_SIZE
		column += CELL_SIZE
		row = 0

def drawBarrier():
	"""Draws a barrier once the user clicks on a valid cell 
	and sets the corresponding nodes barrier attribute to True.
	"""
	# Find the column and row of the cell the user clicks on
	coordinates = pygame.mouse.get_pos()

	if (coordinates[0] / CELL_SIZE) < 0:
		column = 0
	else:
		remainder = coordinates[0] % CELL_SIZE
		column = coordinates[0] - remainder

	remainder = coordinates[1] % CELL_SIZE
	row = coordinates[1] - remainder

	"""Convert column and row coordinates to int values
	corresponding to the x and y values in the MATRIX 2D-Array.
	"""
	x = int(column / CELL_SIZE)
	y = int(row / CELL_SIZE)

	"""Error handling in the case the user attempts to set
	the Start or End Nodes as a barrier.
	"""
	if (x == START_NODE["x"] and y == START_NODE["y"]):
		return
	elif (x == END_NODE["x"] and y == END_NODE["y"]):
		return

	rect = pygame.Rect(column, row, CELL_SIZE, CELL_SIZE)
	
	pygame.draw.rect(SCREEN, BLACK, rect)
	pygame.draw.rect(SCREEN, BLACK, rect, 1)

	MATRIX[x][y]['barrier'] = True

def findNeighbors(node):
	"""Returns the neighboring nodes of a cell as a list object.

	Graph movement is limited to 4 directions; North, South, East,
	and West.
	"""
	maxColSize = WINDOW_WIDTH / CELL_SIZE
	maxRowSize = WINDOW_HEIGHT / CELL_SIZE

	neighbors = []

	if (node["y"] + 1 < maxRowSize):
		x = node["x"]
		y = node["y"] + 1
		neighborSouth = MATRIX[x][y]
		neighbors.append(neighborSouth)

	if (node["y"] - 1 >= 0):
		x = node["x"]
		y = node["y"] - 1
		neighborNorth = MATRIX[x][y]
		neighbors.append(neighborNorth)

	if (node["x"] + 1 < maxColSize):
		x = node["x"] + 1
		y = node["y"] 
		neighborEast = MATRIX[x][y]
		neighbors.append(neighborEast)

	if (node["x"] - 1 >= 0):
		x = node["x"] - 1
		y = node["y"]
		neighborWest = MATRIX[x][y]
		neighbors.append(neighborWest)

	return neighbors

def initCells():
	"""Initializes each cell of a 2D-Array to falsy values."""
	matrix = [[{"x": col, "y": row, "f": None, "g": None, "h": None, "parent": None, "barrier": False} for row in range(int(WINDOW_HEIGHT / CELL_SIZE))] for col in range(int(WINDOW_WIDTH / CELL_SIZE))]
	return matrix

def calculateFCost(node):
	"""Calculates and sets the F cost of a node."""
	calculateGCost(node)
	calculateHCost(node)
	node["f"] = node["g"] + node["h"]

def calculateGCost(node):
	"""Calculates and sets the G cost of a node."""
	distanceX = 0
	distanceY = 0

	# Calculate the Manhattan distance from the Start Node
	distanceX = abs(node["x"] - START_NODE["x"])
	distanceY = abs(node["y"] - START_NODE["y"])
	node["g"] = distanceX + distanceY

def calculateHCost(node):
	"""Calculates and sets the H cost of a node."""
	distanceX = 0
	distanceY = 0

	# Calculate the Manhattan distance from the End Node
	distanceX = abs(node["x"] - END_NODE["x"])
	distanceY = abs(node["y"] - END_NODE["y"])
	node["h"] = distanceX + distanceY

def findLowestFCost():
	"""Returns the Node with the lowest F cost in OPEN_LIST"""
	lowestVal = 0
	currentNode = {}

	for node in OPEN_LIST:
		if (node != START_NODE):
			lowestVal = node["f"]
			currentNode = node
			break

	for node in OPEN_LIST:
		if (node["f"] < lowestVal):
			lowestVal = node["f"]
			currentNode = node
	
	return currentNode

def setParentNode(neighborNode, currentNode):
	"""Sets a neighbor Nodes parent to the current Node."""
	neighborNode["parent"] = {"x": currentNode["x"], "y": currentNode["y"]}

def findShortestPath():
	"""Finds the shortest path between two Nodes using the A* algorithm."""
	global PATH_FOUND
	# Add start node to open
	OPEN_LIST.append(START_NODE)

	current = START_NODE

	calculateFCost(START_NODE)

	count = 0

	while True:		
		if (count > 0):
			current = findLowestFCost()

		# Remove current from open list
		for node in OPEN_LIST:
			if node == current:
				OPEN_LIST.remove(node)

		# Add current to closed list
		CLOSED_LIST.append(current)

		# Error handling in the case a solution is impossible
		try:
			drawClosedNodes(current["x"], current["y"])
		except KeyError:
			# If there is no solution
			PATH_FOUND = True
			return

		# If the shortest path has been found
		if (current["x"] == END_NODE["x"] and current["y"] == END_NODE["y"]):
			setPathCoords(current)
			PATH_FOUND = True
			break
		
		# Get all of current's neighbors
		neighbors = findNeighbors(current)

		"""If a neighbor is not in the Open list, calculate the F cost
		of the neighbor, set the neighbor's parent to the current Node,
		and add the neighbor to the Open list if it's not already in it."""
		for neighbor in neighbors:
			if (neighbor['barrier'] == True):
				continue

			if (isInClosedList(neighbor["x"], neighbor["y"]) == True):
				continue

			if (isInOpenList(neighbor["x"], neighbor["y"]) == False):
				calculateFCost(neighbor)
				setParentNode(neighbor, current)

			if (isInOpenList(neighbor["x"], neighbor["y"]) == False):
				OPEN_LIST.append(neighbor)
				drawOpenNodes(neighbor["x"], neighbor["y"])

		count += 1

def drawOpenNodes(x, y):
	"""Draws Nodes in the Open_List"""
	# Skip over the Start and End Nodes
	if (x == START_NODE["x"] and y == START_NODE["y"]):
		return
	elif (x == END_NODE["x"] and y == END_NODE["y"]):
		return 

	rect = pygame.Rect(x * 20, y * 20, CELL_SIZE, CELL_SIZE)
	pygame.draw.rect(SCREEN, GREEN, rect)
	pygame.draw.rect(SCREEN, BLACK, rect, 1)
	pygame.display.update(rect)

	# Implemented to allow Nodes to be drawn in real time instead of all at once
	time.sleep(.005)

def drawClosedNodes(x, y):
	"""Draws Nodes in the Closed_List"""
	# Skip over the Start and End Nodes
	if (x == START_NODE["x"] and y == START_NODE["y"]):
		return
	elif (x == END_NODE["x"] and y == END_NODE["y"]):
		return 

	rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
	pygame.draw.rect(SCREEN, RED, rect)
	pygame.draw.rect(SCREEN, BLACK, rect, 1)
	pygame.display.update(rect)

	# Implemented to allow Nodes to be drawn in real time instead of all at once
	time.sleep(.005)

def isInOpenList(x, y):
	"""Returns False if the given x and y coordinates
	are not in OPEN_LIST, and True otherwise.
	"""
	for node in OPEN_LIST:
		if (node["x"] == x and node["y"] == y):
			return True

	return False

def isInClosedList(x, y):
	"""Returns False if the given x and y coordinates
	are not in CLOSED_LIST, and True otherwise.
	"""
	for node in CLOSED_LIST:
		if (node["x"] == x and node["y"] == y):
			return True
	
	return False

def drawShortestPath():
	"""This function draws the shortest path."""
	# Redraw the grid cells
	drawCells()

	cols = int(WINDOW_WIDTH / CELL_SIZE)
	rows = int(WINDOW_HEIGHT / CELL_SIZE)

	for j in range(rows):
		for i in range(cols):
			if MATRIX[i][j]['barrier'] == True:
				rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
				pygame.draw.rect(SCREEN, BLACK, rect)
				pygame.draw.rect(SCREEN, BLACK, rect, 1)

	# Redraw the Start and End nodes
	startRect = pygame.Rect(START_NODE["x"] * CELL_SIZE, START_NODE["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
	endRect = pygame.Rect(END_NODE["x"] * CELL_SIZE, END_NODE["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
	pygame.draw.rect(SCREEN, PURPLE, startRect)
	pygame.draw.rect(SCREEN, BLACK, startRect, 1)
	pygame.draw.rect(SCREEN, PURPLE, endRect)
	pygame.draw.rect(SCREEN, BLACK, endRect, 1)
	pygame.display.update()

	# Draw the shortest path
	for x,y in zip(PATH_NODES_X, PATH_NODES_Y):
		# Skip over the Start Node
		if (x == START_NODE['x'] and y == START_NODE['y']):
			continue

		rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
		pygame.draw.rect(SCREEN, PURPLE, rect)
		pygame.draw.rect(SCREEN, BLACK, rect, 1)
		pygame.display.update(rect)

def setPathCoords(node):
	"""Once the End Node has been found, this function
	iterates through each parent Node and appends the 
	x and y values to the PATH_NODES_X/Y list objects.
	
	The argument Node, is the current Node once the End Node
	has been found.
	"""
	x = node["x"]
	y = node["y"]
	current = node
	while current['parent'] != None:
		x = current['parent']['x']
		y = current['parent']['y']

		PATH_NODES_X.append(x)
		PATH_NODES_Y.append(y)

		current = MATRIX[x][y]

def drawStartEndNodes():
	"""Draws the Start and End Nodes."""
	global START_NODE_SET, END_NODE_SET
	global START_NODE, END_NODE

	# Return if the Nodes have already been set
	if START_NODE_SET == True and END_NODE_SET == True:
		return
	
	# Find the column and row of the cell the user clicks on
	coordinates = pygame.mouse.get_pos()

	if (coordinates[0] / CELL_SIZE) < 0:
		column = 0
	else:
		remainder = coordinates[0] % CELL_SIZE
		column = coordinates[0] - remainder

	remainder = coordinates[1] % CELL_SIZE
	row = coordinates[1] - remainder

	# If the user attempts to set the End Node to the same cell as the Start Node
	if START_NODE_SET == True and END_NODE_SET == False:
		x = int(column / CELL_SIZE)
		y = int(row / CELL_SIZE)

		if x == START_NODE["x"] and y == START_NODE["y"]:
			return

	rect = pygame.Rect(column, row, CELL_SIZE, CELL_SIZE)
	
	pygame.draw.rect(SCREEN, PURPLE, rect)
	pygame.draw.rect(SCREEN, BLACK, rect, 1)

	# Set the x and y values of the nodes
	if START_NODE_SET == False:
		START_NODE_SET = True
		START_NODE["x"] = int(column / CELL_SIZE)
		START_NODE["y"] = int(row / CELL_SIZE)
	elif END_NODE_SET == False:
		END_NODE_SET = True
		END_NODE["x"] = int(column / CELL_SIZE)
		END_NODE["y"] = int(row / CELL_SIZE)

if __name__ == "__main__":
	main()