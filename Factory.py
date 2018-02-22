from WebSocket import WebSocket
import Config

class FactoryType(type):
    @property
    def Config(cls):
        if getattr(cls, '_config', None) is None:
            cls._config = Config
        return cls._config
    @property
    def WebSocketServer(cls):
        if getattr(cls, '_websocketserver', None) is None:
            cls._websocketserver = WebSocket(Config, Camera)
        return cls._websocketserver
    @property
    def Camera(cls):
        if getattr(cls, '_camera', None) is None:
            cls._camera = Camera(Config)
        return cls._camera

class Factory(metaclass=FactoryType):
    pass
