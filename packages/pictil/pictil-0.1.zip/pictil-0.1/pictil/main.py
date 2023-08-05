import os
import re
import random

BASEPATH = os.getcwd()

# Get input from the user. Must be four consecutive numbers that won't cause the rename to overflow.
# @param file_count	{int} the number of valid files
# @return {str} the users input starting number
def get_number(file_count):
	inputNumber = str(input(" > Enter the starting number ####: "))
	while (not (re.match(r'[0-9]{4}$', inputNumber) and
			   ((file_count + int(inputNumber)) <= 10000))):
		inputNumber = str(input(" > Enter the starting number ####: "))
	return inputNumber

# The name of the file being tested.
# @param file_name	{str} name of the file
# @return {bool} True if the file is valid; False otherwise
def valid_file(file_name):
	result = False
	if (len(file_name) == 12):
		result = (file_name.endswith(".JPG") or file_name.endswith(".MOV"))
		result = result and file_name.startswith("DSC_")
		for charPos in range(4, 8, 1):
			result = result and (file_name[charPos] >= '0' and file_name[charPos] <= '9')
	return  result

# Generate a random 24 character temporary file name.
# @return {str} the temporary file name
def random_name():
	temp_name = ""
	for i in range(0, 25, 1):
		temp_name = temp_name[:0] + str(random.randint(65, 90)) + temp_name[0:]
	return temp_name

# Generate a replacement file name.
# @param file_name	{str} the name of the file being replaced
# @param new_number	{int} the new number of the file being replaced
# @return {str} replacement file name
def replace_name(file_name, new_number):
	extension = ".JPG" if file_name.endswith(".JPG") else ".MOV"
	new_name = "DSC_"
	temp_new_number = new_number
	for charPos in range(7, 3, -1):
		new_name = new_name[:4] + str(temp_new_number % 10) + new_name[4:]
		temp_new_number = int(temp_new_number / 10)
	new_name = new_name[:8] + extension
	return new_name

# Run the pogram out of this method.
def main():
	    	# Create list of valid files
	    	file_list = []
	    	for fname in os.listdir(BASEPATH):
	    		if (os.path.isfile(os.path.join(BASEPATH, fname)) and valid_file(fname)):
	    			file_list.append(fname)

	    	print("")

	    	# Get the input from the user
	    	input_number = int(get_number(len(file_list)))

	    	print("")

	    	print("   -------------------------------")
	    	print(" > The starting number is: ", input_number)
	    	print("   -------------------------------")

	    	print(" > Preparing Files")
	    	print("   -------------------------------\n")

	    	temp_names = []
	    	# Rename the files to random temporary names
	    	for fname in file_list:
	    		temp_name = random_name()
	    		# if the temp name is already in use, make a new one
	    		while temp_name in temp_names:
	    			temp_name = random_name()
	    		temp_names.append(temp_name)
	    		os.rename(fname, temp_name)

	    	# Rename the files to the new desired numbers
	    	for i in range(0, len(file_list), 1):
	    		fname = file_list[i]
	    		new_file_name = replace_name(str(fname), int(input_number))
	    		print(" >", os.path.join(BASEPATH, fname)," -> ", os.path.join(BASEPATH, new_file_name))
	    		os.rename(temp_names[i], new_file_name)
	    		input_number = input_number + 1

main()
