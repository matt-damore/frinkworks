import argparse

from frinkworks.metadata.mediainfo import extract_metadata


def main() -> None:

    parser = argparse.ArgumentParser(description="Extract media metadata using MediaInfo")

    parser.add_argument("file_path", help="Path to the media file")

    parsed = parser.parse_args()

    metadata = extract_metadata(parsed.file_path)

    print(f"MediaInfo version: {metadata['creatingLibrary']['version']}")
    print(f"File: {metadata['media']['@ref']}")
    print()

    for track in metadata["media"]["track"]:
        track_type = track["@type"]
        track_format = track.get("Format", "Unknown")

        print(f"{track_type}: {track_format}")


if __name__ == "__main__":
    main()
