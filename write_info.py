ERROR_LEVEL=5
def write_info(level, message):
	if(level <= ERROR_LEVEL):
		print(message)
