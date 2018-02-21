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
            cls._websocketserver = WebSocket(Config)
        return cls._websocketserver

class Factory(metaclass=FactoryType):
    pass
