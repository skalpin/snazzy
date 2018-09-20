import util
import assemble
import printer

images = []
images.append(util.process('1.jpg', 1040))
images.append(util.process('2.jpg', 1040))
images.append(util.process('3.jpg', 1040))

filename = assemble.assemble(images)
print(filename)
#printer.print_file(filename)
print('success')

