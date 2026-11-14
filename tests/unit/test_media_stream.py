from uuid import UUID, uuid4

import pytest

from frinkworks.domain.metadata import MediaStream


@pytest.fixture
def report_id():
    """Provide a parent metadata report identifier."""
    return uuid4()


def test_media_stream_creation():
    """A stream preserves its classification, index, and metadata."""
    raw_metadata = {
        "@type": "Video",
        "Format": "HEVC",
        "Width": "1920",
        "Height": "1080",
        "BitDepth": "10",
    }

    stream = MediaStream(
        stream_type="Video",
        stream_index=1,
        raw_metadata=raw_metadata,
        report_id=report_id,
    )

    assert stream.stream_type == "Video"
    assert stream.stream_index == 1
    assert stream.raw_metadata == raw_metadata
    assert stream.report_id == report_id
    assert isinstance(stream.stream_id, UUID)


def test_media_stream_unique_identifiers(report_id):
    """Each stream receives its own identifier."""
    stream_a = MediaStream(
        stream_type="Audio",
        stream_index=2,
        raw_metadata={"Format": "PCM"},
        report_id=report_id,
    )
    stream_b = MediaStream(
        stream_type="Audio",
        stream_index=3,
        raw_metadata={"Format": "PCM"},
        report_id=report_id,
    )

    assert stream_a.stream_id != stream_b.stream_id
    assert stream_a.report_id == stream_b.report_id


def test_media_stream_preserves_unknown_fields():
    """Unrecognized metadata fields are retained."""
    raw_metadata = {
        "@type": "Other",
        "Format": "TimeCode",
        "TimeCode_FirstFrame": "01:00:00:00",
        "Vendor_Specific_Field": "Custom value",
    }

    stream = MediaStream(
        stream_type="Other",
        stream_index=4,
        raw_metadata=raw_metadata,
        report_id=report_id,
    )

    assert stream.raw_metadata == raw_metadata
    assert stream.raw_metadata["Vendor_Specific_Field"] == "Custom value"


def test_media_stream_supports_unfamiliar_types():
    """Stream types are not restricted to a predefined enumeration."""
    stream = MediaStream(
        stream_type="CustomData",
        stream_index=5,
        raw_metadata={"@type": "CustomData"},
        report_id=report_id,
    )

    assert stream.stream_type == "CustomData"
