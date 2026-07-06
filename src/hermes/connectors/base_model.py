from abc import abstractmethod, ABC

class Connector(ABC):

    @abstractmethod
    def fetch():
        pass

    @abstractmethod
    def validate():
        pass
    
    @abstractmethod
    def mapper():
        pass

    @abstractmethod
    def store():
        pass