class AuthorAlreadyExistsError(Exception):
    def __init__(self, email: str):
        super().__init__(f"Author with email '{email}' already exists.")


class AuthorNotFoundError(Exception):
    def __init__(self, author_id: int):
        super().__init__(f"Author with ID {author_id} not found.")
