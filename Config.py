from struct import Struct
native_str = str
str = type('')

WIDTH = 640
HEIGHT = 480
FRAMERATE = 30
HTTP_PORT = 8082
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#333'
HFLIP = True
VFLIP = False
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct(native_str('>4sHH'))
