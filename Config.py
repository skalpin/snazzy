from struct import Struct
native_str = str
str = type('')

WIDTH = 640
HEIGHT = 480
#WIDTH = 1920
#HEIGHT = 1440
#WIDTH = 2048
#HEIGHT = 1563
#WIDTH = 2448
#HEIGHT = 1836
#WIDTH = 3264
#HEIGHT = 2448

FRAMERATE = 24
#FRAMERATE = 30
HTTP_PORT = 8082
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#333'
HFLIP = True
VFLIP = False
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct(native_str('>4sHH'))
