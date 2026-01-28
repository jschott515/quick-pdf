import dataclasses
import enum
import typing


class QpdfToolType(enum.StrEnum):
    PDF_APPEND = "PDF Append"


@dataclasses.dataclass
class QpdfToolsMetadata:
    name: QpdfToolType
    desc: str
    launch: typing.Callable[[], None]
