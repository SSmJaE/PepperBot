from typing import Dict


class AdapaterBase:
    @staticmethod
    def preprocess_event(raw_event: Dict) -> ...:
        """将各个协议的事件，转换为统一的PepperBot事件"""
        pass

    def call_api(self):
        pass

    @staticmethod
    async def dispatch_event_to_handler(event_name: str, raw_event: Dict):
        pass
