import json
import subprocess
from unittest.mock import patch

import pytest

from frinkworks.metadata.mediainfo import MediaInfoError, extract_metadata


@pytest.fixture
def media_file(tmp_path):
    """Create a temporary file for metadata extraction tests."""
    path = tmp_path / "sample.mp4"
    path.write_bytes(b"synthetic test data")
    return path


@pytest.fixture
def valid_metadata():
    """Provide representative MediaInfo JSON metadata."""
    return {
        "creatingLibrary": {
            "name": "MediaInfoLib",
            "version": "26.10",
        },
        "media": {
            "track": [
                {"@type": "General", "Format": "MPEG-4"},
                {"@type": "Video", "Format": "HEVC"},
                {"@type": "Audio", "Format": "AAC"},
            ]
        },
    }


def test_extract_metadata_success(media_file, valid_metadata):
    """Valid MediaInfo JSON is parsed and returned."""
    output = subprocess.CompletedProcess(
        args=["mediainfo"],
        returncode=0,
        stdout=json.dumps(valid_metadata),
        stderr="",
    )

    with patch(
        "frinkworks.metadata.mediainfo.subprocess.run",
        return_value=output,
    ) as mock_run:
        result = extract_metadata(media_file)

    assert result == valid_metadata
    assert len(result["media"]["track"]) == 3

    mock_run.assert_called_once_with(
        ["mediainfo", "--Output=JSON", str(media_file)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        timeout=60,
    )


def test_extract_metadata_missing_file(tmp_path):
    """Missing media files raise FileNotFoundError."""
    missing_file = tmp_path / "missing.mp4"

    with patch("frinkworks.metadata.mediainfo.subprocess.run") as mock_run:
        with pytest.raises(FileNotFoundError, match="Media file not found"):
            extract_metadata(missing_file)

    mock_run.assert_not_called()


def test_extract_metadata_missing_cli(media_file):
    """Missing MediaInfo CLI raises MediaInfoError."""
    with patch(
        "frinkworks.metadata.mediainfo.subprocess.run",
        side_effect=FileNotFoundError("mediainfo not found"),
    ):
        with pytest.raises(MediaInfoError, match="MediaInfo CLI was not found"):
            extract_metadata(media_file)


def test_extract_metadata_timeout(media_file):
    """MediaInfo timeouts raise MediaInfoError."""
    with patch(
        "frinkworks.metadata.mediainfo.subprocess.run",
        side_effect=subprocess.TimeoutExpired(
            cmd=["mediainfo"],
            timeout=60,
        ),
    ):
        with pytest.raises(MediaInfoError, match="timed out"):
            extract_metadata(media_file)


def test_extract_metadata_process_failure(media_file):
    """Nonzero MediaInfo exit codes raise MediaInfoError."""
    with patch(
        "frinkworks.metadata.mediainfo.subprocess.run",
        side_effect=subprocess.CalledProcessError(
            returncode=1,
            cmd=["mediainfo"],
            stderr="Unable to parse media",
        ),
    ):
        with pytest.raises(MediaInfoError, match="Unable to parse media"):
            extract_metadata(media_file)


def test_extract_metadata_invalid_json(media_file):
    """Malformed MediaInfo output raises MediaInfoError."""
    output = subprocess.CompletedProcess(
        args=["mediainfo"],
        returncode=0,
        stdout="{invalid json",
        stderr="",
    )

    with patch(
        "frinkworks.metadata.mediainfo.subprocess.run",
        return_value=output,
    ):
        with pytest.raises(MediaInfoError, match="invalid JSON"):
            extract_metadata(media_file)


@pytest.mark.parametrize(
    "unexpected_output",
    [
        "[]",
        '"not a dictionary"',
        "null",
        "123",
    ],
)
def test_extract_metadata_unexpected_structure(media_file, unexpected_output):
    """Non-dictionary JSON responses raise MediaInfoError."""
    output = subprocess.CompletedProcess(
        args=["mediainfo"],
        returncode=0,
        stdout=unexpected_output,
        stderr="",
    )

    with patch(
        "frinkworks.metadata.mediainfo.subprocess.run",
        return_value=output,
    ):
        with pytest.raises(
            MediaInfoError,
            match="unexpected JSON structure",
        ):
            extract_metadata(media_file)
