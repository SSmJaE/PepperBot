from pydantic import BaseModel


class User(BaseModel):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # self.userId = kwargs["user_id"]
        # self.aaa = 123

    # def __eq__(self, o: "User") -> bool:
    #     return self.userId == o.userId
