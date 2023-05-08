from typing import Any, Callable, Optional, Sequence, Union, cast

from pepperbot.store.command import (
    CLIArgument,
    CLIOption,
    CommandConfig,
    T_InteractiveStrategy,
)
from pepperbot.store.meta import SubCommandRelation, command_relations_cache
from pepperbot.types import COMMAND_CONFIG, BaseClassCommand, F
from pepperbot.utils.common import get_class_name_from_method

__all__ = (
    "as_command",
    "CLIArgument",
    "CLIOption",
)


def as_command(
    *args,
    need_prefix: Optional[bool] = None,
    prefixes: Optional[Sequence[str]] = None,
    aliases: Optional[Sequence[str]] = None,
    include_class_name: Optional[bool] = None,
    exit_patterns: Optional[Sequence[str]] = None,
    require_at: Optional[bool] = None,
    timeout: Optional[int] = None,
    history_size: Optional[int] = None,
    interactive_strategy: Optional[T_InteractiveStrategy] = None,
    config: Optional[Any] = None,
    concurrency: Optional[bool] = None,
    priority: Optional[int] = None,
    propagation_group: Optional[str] = None,
    **kwargs,
):
    """将一个class注册为指令

    Args:
        args (Any): 不要使用位置参数
        need_prefix (bool): 是否需要指令前缀，默认为False
        prefixes (Sequence[str]): 指令前缀，默认为['/']，其中每一项都会作为正则表达式来匹配，并且会自动加上^
        aliases (Sequence[str]): 指令前缀别名，默认为空，其中每一项都会作为正则表达式来匹配
        include_class_name (bool): 类名本身是否作为指令前缀，默认为True
        exit_patterns (Sequence[str]): 退出指令，默认为['^/exit', '^退出']，其中每一项都会作为正则表达式来匹配
        require_at (bool): 是否需要@机器人，默认为False
        timeout (int): 会话超时时间，单位秒，默认为60
        history_size (int): 保留上一次的raw_event，可以在timeout中复用，默认为1；不然timeout中并没有办法获取到raw_event，因为timeout实在apscheduler中独立调用的
        concurrency (bool): 是否允许并发执行，默认为True，此时，priority可能失效
        priority (int): 优先级，越大越先执行，默认为0，可以通过配合StopPropagation来实现选择性的执行后续的指令
        config (Any): 用于传递一些额外的配置，给指令本身使用；一般要求指令作者通过pydantic来定义，以便于自动处理默认值
        propagation_group (str): 传播组，主要影响StopPropagation的行为，如果不同的指令在同一个传播组中，那么StopPropagation会停止同组的指令，但是不会停止其他组的指令

    """

    # 通过locals，自动获取所有kwargs，不手动传入了
    command_kwargs = locals()

    # 只需要具名的参数
    command_kwargs.pop("args")
    command_kwargs.pop("kwargs")

    # 不应包含custom_config
    # custom_config和当前的command_config是绑定的，应该一起传递
    # command_kwargs.pop("config")

    # 去除None，因为pydantic会自动处理默认值
    # 这里为None，就意味着要使用默认值
    # dictionary changed size during iteration
    for kwarg_name, kwarg_value in list(command_kwargs.items()):
        if kwarg_value == None:
            command_kwargs.pop(kwarg_name)

    # 我希望能够点取到as_command的参数，又不希望用户用as_command(CommandConfig(need_prefix=True))这样的形式
    # 所以手动转发一下
    command_config = CommandConfig(**command_kwargs)

    def decorator(class_command: Any):
        initial_method = getattr(class_command, "initial", None)
        if not callable(initial_method):
            raise NotImplementedError(f"指令 {class_command.__name__} 需要实现initial方法作为入口")

        # 需要考虑到多个config的情况
        # class只会缓存一次，但是config可以有多个，所以不能直接覆盖
        saved_command_config = getattr(class_command, COMMAND_CONFIG, {})
        if command_config.config_id not in saved_command_config:
            saved_command_config[command_config.config_id] = command_config

        setattr(class_command, COMMAND_CONFIG, saved_command_config)

        # setattr(class_command, COMMAND_CONFIG, command_config)
        # setattr(class_command, CUSTOM_COMMAND_CONFIG, config)

        return cast(BaseClassCommand, class_command)

    return decorator


def sub_command(
    parent: Optional[Union[Callable, str]] = None, name: Optional[str] = None
):
    def decorator(method: F) -> F:
        method_name: str = method.__name__  # type: ignore

        if method_name not in command_relations_cache:
            parent_method_name: Optional[str] = None
            if parent is not None:
                if isinstance(parent, str):
                    parent_method_name = parent
                else:
                    parent_method_name = parent.__name__

            class_name = get_class_name_from_method(method)

            command_relations_cache[class_name][method_name] = SubCommandRelation(
                parent_method_name=parent_method_name,
                command_final_name=name or method_name,
            )

        return method

    return decorator
