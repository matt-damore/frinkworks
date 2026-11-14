from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class MetadataReport:
    """A complete MediaInfo extraction report"""

    raw_metadata: dict[str, Any]
    extractor_name: str
    extractor_version: str
    report_id: UUID = field(default_factory=uuid4)
    extracted_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class MediaStream:
    """
    Representation for individual streams within a media file.

    A media file can have multiple video, audio, subtitle, timecode and data tracks.
    """

    stream_type: str
    stream_index: int
    raw_metadata: dict[str, Any]

    report_id: UUID
    stream_id: UUID = field(default_factory=uuid4)
