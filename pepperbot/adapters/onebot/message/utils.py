from pepperbot.core.message.chain import T_SegmentInstance
from pepperbot.core.message.segment import Image


def is_flash(segment: T_SegmentInstance) -> bool:
    if not isinstance(segment, Image):
        return False

    if segment.onebot["data"].get("type") == "flash":
        return True
    else:
        return False
