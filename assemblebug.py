import util
import assemble

images = []
images.append(util.process('1.jpg', 1040))
images.append(util.process('2.jpg', 1040))
images.append(util.process('3.jpg', 1040))

print(assemble.assemble(images))
