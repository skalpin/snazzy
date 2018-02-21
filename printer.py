import cups

def print_file(filename):
	conn = cups.Connection()
	printers = conn.getPrinters()
	for printer in printers:
		print(printer, printers[printer]["device-uri"])

	piMate = printers.keys()[0]
	conn.printFile(piMate, filename, "BoothPrint", {})
