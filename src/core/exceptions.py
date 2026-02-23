class NotFoundException(Exception):
    def __init__(self, model: str, id: int):
        self.model = model
        self.id = id

        super().__init__(f"{model} {id} not found")


class BookServiceError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message

        super().__init__(f"{status}: {message}")
