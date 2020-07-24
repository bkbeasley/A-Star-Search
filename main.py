import sys, pygame
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (29, 238, 17)
RED = (238, 17, 29)
BLUE = (18, 235, 255)
DARK_BLUE = (17, 29, 238)
YELLOW = (226, 17, 238)
WINDOW_WIDTH = 640
WINDOW_HEIGHT= 480
CELL_SIZE = 20

def main():
	global SCREEN, CLOCK, START_NODE_SET, END_NODE_SET 
	global START_NODE, END_NODE
	global MATRIX
	global OPEN_LIST, CLOSED_LIST
	global PATH_FOUND
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

	count = 0

	foundCount = 0

	while True:
		events = pygame.event.get()

		if PATH_FOUND:
			if (foundCount < 1):
				showFinalPath()
			foundCount += 1
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == 114:
						drawCells()
						pygame.display.update()
						foundCount = 0
						reset()

			#time.sleep(3)
			#pygame.quit()
			#sys.exit()

		for event in events:
			if event.type == pygame.KEYDOWN:
				# If space bar is pressed down
				if event.key == 32:
					if PATH_FOUND == False:
						runAlgorithm()
					else:
						count += 1
						if count <= 1:
							showFinalPath()
							#drawGrid()
							count = 0

			# If the user clicks the left mouse button down
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					if START_NODE_SET == False or END_NODE_SET == False:
						drawStartNode()
					else:
						if PATH_FOUND == False:
							drawBarrier()
			# Exit
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

def drawGrid():
	for x in range(WINDOW_WIDTH):
		for y in range(WINDOW_HEIGHT):
			rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(SCREEN, BLACK, rect, 1)

def reset():
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
	column = 0
	row = 0
	for x in range(WINDOW_WIDTH):
		for y in range(WINDOW_HEIGHT):
			rect = pygame.Rect(column, row, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(SCREEN, WHITE, rect)
			# TEST!!
			pygame.draw.rect(SCREEN, BLACK, rect, 1)
			row += CELL_SIZE
		column += CELL_SIZE
		row = 0

def drawBarrier():
	# Find the column and row of the cell the user clicks on
	coordinates = pygame.mouse.get_pos()
	#print("IN BARRIER: ", coordinates)

	if (coordinates[0] / CELL_SIZE) < 0:
		column = 0
	else:
		remainder = coordinates[0] % CELL_SIZE
		column = coordinates[0] - remainder

	remainder = coordinates[1] % CELL_SIZE
	row = coordinates[1] - remainder

	rect = pygame.Rect(column, row, CELL_SIZE, CELL_SIZE)
	
	pygame.draw.rect(SCREEN, BLACK, rect)
	pygame.draw.rect(SCREEN, BLACK, rect, 1)

	x = int(column / CELL_SIZE)
	y = int(row / CELL_SIZE)

	MATRIX[x][y]['barrier'] = True

def findNeighbors(node):
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
	matrix = [[{"x": col, "y": row, "f": None, "g": None, "h": None, "parent": None, "barrier": False} for row in range(int(WINDOW_HEIGHT / CELL_SIZE))] for col in range(int(WINDOW_WIDTH / CELL_SIZE))]
	return matrix

def calculateFCost(node):
	calculateGCost(node)
	calculateHCost(node)
	node["f"] = node["g"] + node["h"]

def calculateGCost(node):
	# Calculate the Manhattan distance from the Start Node
	distanceX = 0
	distanceY = 0

	distanceX = abs(node["x"] - START_NODE["x"])
	distanceY = abs(node["y"] - START_NODE["y"])
	node["g"] = distanceX + distanceY

def calculateHCost(node):
	# Calculate the Manhattan distance from the End Node
	distanceX = 0
	distanceY = 0

	distanceX = abs(node["x"] - END_NODE["x"])
	distanceY = abs(node["y"] - END_NODE["y"])
	node["h"] = distanceX + distanceY

def findLowestFCost():
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
	neighborNode["parent"] = {"x": currentNode["x"], "y": currentNode["y"]}

def runAlgorithm():
	global PATH_FOUND
	# Add start node to open
	OPEN_LIST.append(START_NODE)

	current = START_NODE

	calculateFCost(START_NODE)
	#setParentNode(START_NODE, START_NODE)

	count = 0

	while True:
		
		if (count > 0):
			current = findLowestFCost()
		
		#print("CURRENT NODE: ", current)
		#print("OPEN LIST BEFORE: ", OPEN_LIST)
		# Remove current from open list
		for node in OPEN_LIST:
			if node == current:
				OPEN_LIST.remove(node)

		#print("OPEN LIST AFTER: ", OPEN_LIST)
		# Add current to closed list
		CLOSED_LIST.append(current)
		try:
			drawClosed(current["x"], current["y"])
		except KeyError:
			# If there is no solution
			PATH_FOUND = True
			return

		#print("CLOSED LIST: ", CLOSED_LIST)
		# If the shortest path has been found
		if (current["x"] == END_NODE["x"] and current["y"] == END_NODE["y"]):
			#findPath()
			print("FINISHED!!!!!!!!!!")
			#print(current)
			displayPath(current)
			PATH_FOUND = True
			break
		
		# Get all of current's neighbors
		neighbors = findNeighbors(current)
		#print("NEIGHBORS: ", neighbors)

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
				drawOpen(neighbor["x"], neighbor["y"])

			#print("CURRENT NEIGHBOR: ", neighbor)
		count += 1

def displayOpenNodes():
	if not OPEN_LIST:
		return
	
	for node in OPEN_LIST:
		#print("NODE: ", node)
		rect = pygame.Rect(node["x"] * 20, node["y"] * 20, CELL_SIZE, CELL_SIZE)
		pygame.draw.rect(SCREEN, GREEN, rect)
	

def drawOpen(x, y):
	if (x == START_NODE["x"] and y == START_NODE["y"]):
		return
	elif (x == END_NODE["x"] and y == END_NODE["y"]):
		return 

	rect = pygame.Rect(x * 20, y * 20, CELL_SIZE, CELL_SIZE)
	pygame.draw.rect(SCREEN, GREEN, rect)
	pygame.draw.rect(SCREEN, BLACK, rect, 1)
	pygame.display.update(rect)
	time.sleep(.005)

def drawClosed(x, y):
	if (x == START_NODE["x"] and y == START_NODE["y"]):
		return
	elif (x == END_NODE["x"] and y == END_NODE["y"]):
		return 

	rect = pygame.Rect(x * 20, y * 20, CELL_SIZE, CELL_SIZE)
	pygame.draw.rect(SCREEN, RED, rect)
	pygame.draw.rect(SCREEN, BLACK, rect, 1)
	pygame.display.update(rect)
	time.sleep(.005)

def isInOpenList(x, y):
	for n in OPEN_LIST:
		if (n["x"] == x and n["y"] == y):
			return True

	return False

def isInClosedList(x, y):
	for n in CLOSED_LIST:
		if (n["x"] == x and n["y"] == y):
			return True
	
	return False

def showFinalPath():
	drawCells()
	#drawGrid()

	cols = int(WINDOW_WIDTH / CELL_SIZE)
	rows = int(WINDOW_HEIGHT / CELL_SIZE)

	for j in range(rows):
		for i in range(cols):
			if MATRIX[i][j]['barrier'] == True:
				rect = pygame.Rect(i * 20, j * 20, CELL_SIZE, CELL_SIZE)
				pygame.draw.rect(SCREEN, BLACK, rect)
				pygame.draw.rect(SCREEN, BLACK, rect, 1)


	startRect = pygame.Rect(START_NODE["x"] * CELL_SIZE, START_NODE["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
	endRect = pygame.Rect(END_NODE["x"] * CELL_SIZE, END_NODE["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
	pygame.draw.rect(SCREEN, YELLOW, startRect)
	pygame.draw.rect(SCREEN, BLACK, startRect, 1)
	pygame.draw.rect(SCREEN, YELLOW, endRect)
	pygame.draw.rect(SCREEN, BLACK, endRect, 1)
	pygame.display.update()
	for x,y in zip(PATH_NODES_X, PATH_NODES_Y):
		if (x == START_NODE['x'] and y == START_NODE['y']):
			continue
		rect = pygame.Rect(x * 20, y * 20, CELL_SIZE, CELL_SIZE)
		pygame.draw.rect(SCREEN, DARK_BLUE, rect)
		pygame.draw.rect(SCREEN, BLACK, rect, 1)
		pygame.display.update(rect)


def displayPath(node):
	x = node["x"]
	y = node["y"]
	current = node
	while current['parent'] != None:
		#print("X: ", x, " Y: ", y)
		x = current['parent']['x']
		y = current['parent']['y']

		PATH_NODES_X.append(x)
		PATH_NODES_Y.append(y)

		current = MATRIX[x][y]

	#for n in node:
		#print(n['parent'][0]['parent'])
	""" for item in node:
		for key, value in item.items():
			if key == 'parent':
				print("AA: ", value['x']) """
				#rect = pygame.Rect(node["x"] * 20, node["y"] * 20, CELL_SIZE, CELL_SIZE)
				#pygame.draw.rect(SCREEN, RED, rect)
			


def drawStartNode():
	global START_NODE_SET, END_NODE_SET
	global START_NODE, END_NODE

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
	
	pygame.draw.rect(SCREEN, YELLOW, rect)
	pygame.draw.rect(SCREEN, BLACK, rect, 1)

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