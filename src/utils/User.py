class User:
    def __init__(self, **kwargs) -> None:
        self.userId = kwargs['user_id']

    def __eq__(self, o: "User") -> bool:
        return self.userId == o.userId
