from typing import Any, Callable, Coroutine, Dict, List, Optional

from pydantic import BaseModel, BaseSettings


class GPTExampleConfig(BaseModel):
    proxy_call: Optional[Callable[[List[Dict]], Coroutine[Any, Any, str]]] = None
    """ 如何调用GPT，输入messages，返回当前的completion """


class GPTExampleSetting(BaseSettings):
    class Config:
        env_file = ".env"  # 必须手动指定
        env_file_encoding = "utf-8"
        env_prefix = "gpt_example_"
        env_nested_delimiter = "__"

    token: Optional[str] = None
    """ openai的token 
    
    直接提供token + proxy_token，或者自己实现proxy_call，二选一
    """
    proxy_token: Optional[str] = None
    """ 如果使用群内的GPT代理，需要提供token，证明是PepperBot群员，避免滥用 """
    default_times: int = 5
    """ 每天每个用户最多调用次数，通过设置interactive_strategy跨群锁定用户 
    
    如果未在times_per_group中设置，则使用此值
    """
    times_per_group: Dict[str, int] = {}
    """ 
    { "group_id" : 每天每个用户最多调用次数 }，通过设置interactive_strategy跨群锁定用户
    """
    times_per_user: Dict[str, int] = {}
    """
    { "user_id" : 每天每个用户最多调用次数 }，通过设置interactive_strategy跨群锁定用户
    """
    super_groups: List[str] = []
    """ 超级群，不受次数限制 """
    super_users: List[str] = []
    """ 超级用户，不受次数限制 """


gpt_example_setting = GPTExampleSetting()
