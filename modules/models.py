# ============================================================
# modules/models.py
# NASA API 반환 타입 dataclass
# ============================================================

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class NasaImage:
    title:       str
    img_url:     str
    description: str
    media_type:  str
    date:        str = ""
    keyword:     str = ""
    source_type: str = ""
    source_id:   str = ""


@dataclass
class FetchResult:
    data:  NasaImage | None
    error: str | None

    @property
    def ok(self) -> bool:
        return self.data is not None and self.error is None
