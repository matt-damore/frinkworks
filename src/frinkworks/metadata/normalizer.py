from copy import deepcopy
from typing import Any

from frinkworks.domain.metadata import MediaStream, MetadataReport


def build_metadata_report(raw_metadata: Any) -> tuple[MetadataReport, list[MediaStream]]:
    if not isinstance(raw_metadata, dict):
        raise ValueError("MediaInfo metadata must be a dictionary")

    creating_library = raw_metadata.get("creatingLibrary")

    if not isinstance(creating_library, dict):
        raise ValueError("Missing or invalid creatingLibrary section")

    version = creating_library.get("version")

    if not isinstance(version, str) or not version.strip():
        raise ValueError("Missing or invalid MediaInfo version")

    media = raw_metadata.get("media")

    if not isinstance(media, dict):
        raise ValueError("Missing or invalid media section")

    track = media.get("track")

    if not isinstance(track, list):
        raise ValueError("Missing or invalid track list")

    metadata_snapshot = deepcopy(raw_metadata)

    metadata_report = MetadataReport(
        raw_metadata=metadata_snapshot,
        extractor_name="MediaInfo",
        extractor_version=version,
    )

    streams: list[MediaStream] = []

    for index, track_data in enumerate(track):
        if not isinstance(track_data, dict):
            raise ValueError(f"Track at index {index} must be a dictionary")

        stream_type = track_data.get("@type")

        if not isinstance(stream_type, str) or not stream_type.strip():
            raise ValueError(f"Missing or invalid @type for track at index {index}")

        stream = MediaStream(
            stream_type=stream_type,
            stream_index=index,
            raw_metadata=deepcopy(track_data),
            report_id=metadata_report.report_id,
        )

        streams.append(stream)

    return metadata_report, streams
