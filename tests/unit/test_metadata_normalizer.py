from copy import deepcopy

import pytest

from frinkworks.domain.metadata import MediaStream, MetadataReport
from frinkworks.metadata.normalizer import build_metadata_report


@pytest.fixture
def valid_metadata():
    """Representative MediaInfo JSON with multiple stream types."""
    return {
        "creatingLibrary": {
            "name": "MediaInfoLib",
            "version": "26.10",
        },
        "media": {
            "@ref": "sample.mov",
            "track": [
                {"@type": "General", "Format": "QuickTime"},
                {
                    "@type": "Video",
                    "Format": "ProRes",
                    "Width": "3840",
                    "Height": "2160",
                },
                {"@type": "Audio", "Format": "PCM", "Channels": "2"},
                {"@type": "Audio", "Format": "PCM", "Channels": "6"},
                {
                    "@type": "Other",
                    "Format": "TimeCode",
                    "TimeCode_FirstFrame": "01:00:00:00",
                    "Vendor_Specific_Field": "Preserve this",
                },
            ],
        },
    }


def test_normalizer_creates_report(valid_metadata):
    """Normalizer creates a report with complete original metadata."""
    report, streams = build_metadata_report(valid_metadata)

    assert isinstance(report, MetadataReport)
    assert report.extractor_name == "MediaInfo"
    assert report.extractor_version == "26.10"
    assert report.raw_metadata == valid_metadata
    assert isinstance(streams, list)


def test_normalizer_preserves_stream_order(valid_metadata):
    """All tracks are represented in their original order."""
    report, streams = build_metadata_report(valid_metadata)

    assert len(streams) == 5
    assert all(isinstance(stream, MediaStream) for stream in streams)
    assert [stream.stream_type for stream in streams] == [
        "General",
        "Video",
        "Audio",
        "Audio",
        "Other",
    ]
    assert [stream.stream_index for stream in streams] == [0, 1, 2, 3, 4]


def test_normalizer_links_streams_to_report(valid_metadata):
    """Every stream belongs to the report that produced it."""
    report, streams = build_metadata_report(valid_metadata)

    assert all(stream.report_id == report.report_id for stream in streams)
    assert len({stream.stream_id for stream in streams}) == len(streams)


def test_normalizer_preserves_unknown_fields(valid_metadata):
    """Vendor-specific metadata is retained without modification."""
    report, streams = build_metadata_report(valid_metadata)

    assert streams[4].raw_metadata["Vendor_Specific_Field"] == "Preserve this"
    assert streams[4].raw_metadata == valid_metadata["media"]["track"][4]


@pytest.mark.parametrize(
    "invalid_metadata",
    [
        None,
        [],
        {},
        {"creatingLibrary": {"version": "26.10"}},
        {
            "creatingLibrary": {"version": "26.10"},
            "media": {"track": "not a list"},
        },
        {
            "creatingLibrary": {"version": "26.10"},
            "media": {"track": [{"Format": "HEVC"}]},
        },
        {
            "creatingLibrary": {"version": "26.10"},
            "media": {"track": [None]},
        },
    ],
)
def test_normalizer_rejects_invalid_metadata(invalid_metadata):
    """Malformed metadata structures raise ValueError."""
    with pytest.raises(ValueError):
        build_metadata_report(invalid_metadata)


def test_normalizer_preserves_input_snapshot(valid_metadata):
    """Changes to the input must not alter an existing report."""

    report, streams = build_metadata_report(valid_metadata)

    original_report = deepcopy(report.raw_metadata)
    original_stream = deepcopy(streams[1].raw_metadata)

    valid_metadata["media"]["track"][1]["Format"] = "H.264"

    assert report.raw_metadata == original_report
    assert streams[1].raw_metadata == original_stream


def test_stream_mutation_does_not_affect_report(valid_metadata):
    """Modifying a stream must not change the parent report."""
    report, streams = build_metadata_report(valid_metadata)

    original_format = report.raw_metadata["media"]["track"][1]["Format"]

    streams[1].raw_metadata["Format"] = "Modified"

    assert report.raw_metadata["media"]["track"][1]["Format"] == original_format
