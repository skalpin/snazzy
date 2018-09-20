import cups

def print_file(filename):
	print(filename)
	conn = cups.Connection()
	printers = conn.getPrinters()
	for printer in printers:
		print(printer, printers[printer]["device-uri"])

	piMate = list(printers.keys())[0]
	conn.printFile(piMate, filename, "BoothPrint", {})
