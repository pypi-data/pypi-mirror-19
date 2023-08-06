class Context:
    def __init__(self, room_id, client_id):
        self.room_id = room_id
        self.client_id = client_id


class ContextEngine:

    def run(self):
        pass

    def get_context(self, room_id, client_id):
        pass

    def update_context(self, room_id, client_id):
        pass


class InMemoryContextEngine(ContextEngine):

    def __init__(self):
        self.__context = []

    def get_context(self, room_id, client_id):
        pass