from pepperbot.message.segment import Image
from pepperbot.message.chain import SegmentInstance_T


def is_flash(segment: SegmentInstance_T) -> bool:
    if not isinstance(segment, Image):
        return False

    if segment.formatted["data"].get("type") == "flash":
        return True
    else:
        return False
