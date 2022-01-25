class OnebotV11SpecificCommonApi:
    pass


class OnebotV11SpecificGroupApi:
    pass


class OnebotV11SpecificPrivateApi:
    pass


class KeaimaoSpecificApi:
    pass


class UniversalCommonApi:
    pass


class UniversalGroupApi:
    pass


class UniversalPrivateApi:
    pass


class OnebotV11Api:
    pass


class KeaimaoApi:
    pass


class GroupBot(UniversalCommonApi, UniversalGroupApi):
    __slots__ = (
        "from_onebot",
        "from_keaimao",
        "from_telegram",
        "group_id",
        "bot_id",
        "onebot",
        "keaimao",
    )

    def __init__(
        self,
        from_onebot: bool,
        from_keaimao: bool,
        from_telegram: bool,
        group_id: str,
        bot_id: str,
        onebot: OnebotV11Api,
        keaimao: KeaimaoApi,
    ):
        self.from_onebot = from_onebot
        self.from_keaimao = from_keaimao
        self.from_telegram = from_telegram

        self.group_id = group_id
        self.bot_id = bot_id

        self.onebot = onebot
        self.keaimao = keaimao

    # @property
    # def api_caller(self):
    #     if self.from_onebot:
    #         return get_onebot_api_caller()
    #     elif self.from_keaimao:
    #         return get_keaimao_api_caller()

    # async def group_msg(
    #     self, targetGroupId: Union[int, SegmentInstance_T], *chain: SegmentInstance_T
    # ):
    #     if isinstance(targetGroupId, int):
    #         groupId = targetGroupId
    #         message = [segment.formatted for segment in chain]
    #     else:
    #         groupId = self.groupId
    #         message = [
    #             targetGroupId.formatted,
    #             *[segment.formatted for segment in chain],
    #         ]

    #     if self.from_onebot:
    #         await OnebotV11Adapter.group_msg()

    #         # await self.api_caller.call(
    #         #     "send_group_msg",
    #         #     **{
    #         #         "group_id": groupId,
    #         #         "message": message,
    #         #     },
    #         # )
    #     elif self.from_keaimao:
    #         await KeaimaoAdapter.group_msg()
    #         # await self.api_caller.call(
    #         #     "groupMessage",
    #         #     {},
    #         # )
    #     elif self.from_telegram:
    #         pass
