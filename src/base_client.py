from utils.singleton_meta import Singleton


class BookstoreClient(metaclass=Singleton):
    def __init__(self, base_url: str):
        self.base_url = base_url
