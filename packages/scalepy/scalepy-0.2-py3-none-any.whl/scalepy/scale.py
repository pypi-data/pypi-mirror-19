import sys
import re

# Print the transition from the old x,y to the new x,y
# @param oldX	{int} original x dimension
# @param oldY	{int} oritinal y dimension
# @param newX	{int} scaled x dimension
# @param newY	{int} scaled y dimension
def print_new_size(oldX, oldY, newX, newY):
	print (" > {}x{} -> {}x{}".format(oldX, oldY, newX, newY))

# Calculate the resized x dimension based on the given y dimension
# @param oldX	{int} original x dimension
# @param oldY	{int} oritinal y dimension
# @param newY	{int} determined y dimension
def resize_x(oldX, oldY, newY):
	return int(round(((oldX * newY)/oldY), 0))

# Calculate the resized x dimension based on the given y dimension
# @param oldX	{int} original x dimension
# @param oldY	{int} oritinal y dimension
# @param newY	{int} determined x dimension
def resize_y(oldX, oldY, newX):
	return int(round(((oldY * newX)/oldX), 0))

# Calculate the resized x dimension based on the given y dimension
# @param oldX	{int} original x dimension
# @param oldY	{int} oritinal y dimension
# @param scale	{int} dimension scale
def resize_s(oldX, oldY, scale):
	scale = float(scale) / 100.0
	return [int(round(oldX * scale, 0)), int(round(oldY * scale, 0))]

# Run the program out of this message
def scale():

	print()

	arg_r = re.compile('^-[xys]$')
	val_r = re.compile('^[0-9]*$')

	arguments = sys.argv[1:]

	if (not len(arguments) == 4):
		print("Invalid Argument Count")
		sys.exit(1)
	if (not re.match(arg_r, arguments[0])):
		print("Invalid Modifier: ", arguments[0])
		sys.exit(1)
	for arg in arguments[1:]:
		if (not re.match(val_r, arg)):
			print("Invalid Argument: ", arg)
			sys.exit(1)

	x = int(arguments[3])
	y = int(arguments[3])

	# If -y argument, then the scaled y dimension is given
	if (re.match(r'-y', arguments[0])):
		x = resize_x(int(arguments[1]), int(arguments[2]), int(arguments[3]))

	# If -x argument, then the scaled x dimension is given
	if (re.match(r'-x', arguments[0])):
		y = resize_y(int(arguments[1]), int(arguments[2]), int(arguments[3]))

	# If -s argument, then a scale to be applied to both dimensions is given
	if (re.match(r'-s', arguments[0])):
		vals = resize_s(int(arguments[1]), int(arguments[2]), int(arguments[3]))
		x = vals[0]
		y = vals[1]

	print_new_size(int(arguments[1]), int(arguments[2]), x, y)
