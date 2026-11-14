from datetime import datetime
from uuid import UUID

from frinkworks.domain.metadata import MetadataReport


def test_metadata_report_creation():
    """A metadata report stores its extractor information and raw JSON."""
    raw_metadata = {
        "media": {
            "track": [
                {"@type": "General", "Format": "MPEG-4"},
                {"@type": "Video", "Format": "HEVC"},
                {"@type": "Audio", "Format": "AAC"},
            ]
        }
    }

    report = MetadataReport(
        raw_metadata=raw_metadata,
        extractor_name="MediaInfo",
        extractor_version="26.10",
    )

    assert report.raw_metadata == raw_metadata
    assert report.extractor_name == "MediaInfo"
    assert report.extractor_version == "26.10"
    assert isinstance(report.report_id, UUID)
    assert isinstance(report.extracted_at, datetime)


def test_metadata_report_unique_identifiers():
    """Each report receives a distinct identifier."""
    report_a = MetadataReport({}, "MediaInfo", "26.10")
    report_b = MetadataReport({}, "MediaInfo", "26.10")

    assert report_a.report_id != report_b.report_id


def test_metadata_report_utc_timestamp():
    """Extraction timestamps are timezone-aware and use UTC."""
    report = MetadataReport({}, "MediaInfo", "26.10")

    assert report.extracted_at.tzinfo is not None
    assert report.extracted_at.utcoffset().total_seconds() == 0


def test_metadata_report_preserves_all_tracks():
    """Reports retain multiple tracks and unfamiliar metadata fields."""
    raw_metadata = {
        "creatingLibrary": {"version": "26.10"},
        "media": {
            "track": [
                {"@type": "Video", "Format": "HEVC", "BitDepth": "10"},
                {"@type": "Audio", "Format": "PCM", "Channels": "2"},
                {"@type": "Audio", "Format": "PCM", "Channels": "6"},
                {
                    "@type": "Other",
                    "Format": "TimeCode",
                    "TimeCode_FirstFrame": "01:00:00:00",
                    "Custom_Field": "Preserve this value",
                },
            ]
        },
    }

    report = MetadataReport(raw_metadata, "MediaInfo", "26.10")

    assert report.raw_metadata == raw_metadata
    assert len(report.raw_metadata["media"]["track"]) == 4
    assert report.raw_metadata["media"]["track"][3]["Custom_Field"] == ("Preserve this value")
