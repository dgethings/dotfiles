# /// script
# dependencies = [
#     "dotenv>=0.9.9",
#     "requests>=2.32.5",
#     "youtube-transcript-api>=1.2.3",
# ]
# ///

import unicodedata
import json
import os
import re
import sys
import uuid
from typing import Any

import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)
from urllib.parse import urlparse, parse_qs

DEBUG = os.getenv("DEBUG", False)


def return_id(url: str) -> str:
    yt_url = urlparse(url)

    if "youtu.be" in yt_url.netloc:
        return yt_url.path.lstrip("/").split("?")[0].split("&")[0]

    if "youtube.com" in yt_url.netloc:
        if yt_url.path == "/watch":
            param = parse_qs(yt_url.query)
            return param.get("v", [""])[0]
        elif (
            yt_url.path.startswith("/v/")
            or yt_url.path.startswith("/embed/")
            or yt_url.path.startswith("/e/")
        ):
            return yt_url.path.split("/")[-1].split("?")[0]
        elif yt_url.path.startswith("/shorts/") or yt_url.path.startswith("/live/"):
            return yt_url.path.split("/")[-1].split("?")[0]
        elif yt_url.path == "/oembed":
            param = parse_qs(yt_url.query)
            url_param = param.get("url", [""])[0]
            return return_id(url_param)
        elif yt_url.path == "/attribution_link":
            param = parse_qs(yt_url.query)
            u_param = param.get("u", [""])[0]
            parsed_u = urlparse(u_param)
            param_u = parse_qs(parsed_u.query)
            return param_u.get("v", [""])[0]
    elif "youtube-nocookie.com" in yt_url.netloc:
        return yt_url.path.split("/")[-1].split("?")[0]

    return ""


def sanitize_title(title: str) -> str:
    """Sanitize a video title for use in filenames and display.

    This function performs the exact same sanitization steps as the original
    TypeScript implementation to ensure consistency.

    Args:
        title: Raw video title from YouTube

    Returns:
        Sanitized title safe for filesystem use

    Examples:
        >>> sanitize_title("Never Gonna Give You Up [Official Video]")
        'Never Gonna Give You Up Official Video'

        >>> sanitize_title("Video: With Special <Characters>")
        'Video- With Special Characters'
    """
    # Normalize Unicode characters (NFC)
    title = unicodedata.normalize("NFC", title)

    # Remove leading brackets [
    title = title.replace("[", "")

    # Remove trailing brackets ]
    title = title.replace("]", "")

    # Replace colons with hyphens
    title = title.replace(":", "-")

    # Remove invalid filename chars and control chars
    # Pattern matches: < > : " / \ | ? * and control characters
    title = re.sub(r'[<>:"/\\|?*\x00-\x1f\x7f-\x9f]', "", title)

    # Remove emojis (basic set)
    title = re.sub(r"[\U0001F600-\U0001F64F]", "", title)

    # Remove symbols & pictographs
    title = re.sub(r"[\U0001F300-\U0001F5FF]", "", title)

    # Remove transport & map symbols
    title = re.sub(r"[\U0001F680-\U0001F6FF]", "", title)

    # Remove flags
    title = re.sub(r"[\U0001F1E0-\U0001F1FF]", "", title)

    # Remove misc symbols
    title = re.sub(r"[\u2600-\u26FF]", "", title)

    # Remove general punctuation
    title = re.sub(r"[\u2000-\u206F]", "", title)

    # Normalize whitespace (collapse to single spaces)
    title = re.sub(r"\s+", " ", title)

    # Trim whitespace
    title = title.strip()

    # Limit length to 100 characters for filesystem compatibility
    title = title[:100]

    return title


def is_safe_filename(title: str) -> bool:
    """Check if a title is safe for use as a filename.

    Args:
        title: Title to check

    Returns:
        True if title is safe, False otherwise
    """
    # Check for invalid filename characters
    if re.search(r'[<>:"/\\|?*\x00-\x1f\x7f-\x9f]', title):
        return False

    # Check for reserved names (Windows)
    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }

    if title.upper() in reserved_names:
        return False

    return True


def create_safe_filename(title: str, extension: str = ".md") -> str:
    """Create a safe filename from a title.

    Args:
        title: Video title to convert
        extension: File extension to append (default: .md)

    Returns:
        Safe filename with extension
    """
    sanitized = sanitize_title(title)

    # Ensure we have a valid filename (empty or just whitespace/hyphens)
    if not sanitized or sanitized.strip("-_ ") == "":
        sanitized = "untitled"

    # Add extension
    if not extension.startswith("."):
        extension = "." + extension

    return sanitized + extension


def validate_youtube_video_id(video_id: str) -> None:
    """Validate YouTube video ID format.

    Args:
        video_id: YouTube video ID to validate

    Raises:
        ValueError: If video ID is invalid
    """
    if not video_id or not isinstance(video_id, str):
        raise ValueError("Video ID must be a non-empty string")

    # YouTube video IDs are typically 11 characters and contain alphanumeric chars, hyphens, and underscores
    valid_id_pattern = re.compile(r"^[a-zA-Z0-9_-]{11}$")
    if not valid_id_pattern.match(video_id):
        raise ValueError("Invalid YouTube video ID format")


def get_youtube_transcript(video_id: str) -> str:
    """Fetch YouTube video transcript using youtube-transcript-api.

    Args:
        video_id: YouTube video ID

    Returns:
        Concatenated transcript text

    Raises:
        Exception: If transcript is not available or fetching fails
    """
    validate_youtube_video_id(video_id)

    if DEBUG:
        print(f"[youtube-transcript] Fetching transcript for video {video_id}")

    try:
        # Try to get transcript with language fallbacks
        # First try English variants, then fall back to any available language
        languages = ["en", "en-US", "en-GB", "en-AU"]

        try:
            # Try English variants first
            transcript_segments = YouTubeTranscriptApi().fetch(
                video_id, languages=languages
            )
        except (NoTranscriptFound, TranscriptsDisabled):
            # Fall back to any available transcript
            transcript_segments = YouTubeTranscriptApi().fetch(video_id)

        # Convert the array of transcript segments to a single concatenated string
        transcript_text = " ".join(
            segment.text for segment in transcript_segments
        ).strip()

        if not transcript_text:
            raise Exception(
                "No transcript available for this video. The video may not have captions or they may not be accessible through the public API."
            )

        return transcript_text

    except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable):
        # Handle library-specific errors and convert to our expected error format
        raise Exception(
            "No transcript available for this video. The video may not have captions or they may not be accessible through the public API."
        )
    except Exception as e:
        # For other errors, include the original message
        raise Exception(f"Failed to fetch transcript: {str(e)}")


def get_youtube_metadata(video_id: str) -> dict[str, str]:
    """Fetch YouTube video metadata using YouTube Data API v3.

    Args:
        video_id: YouTube video ID

    Returns:
        Dictionary containing title and description

    Raises:
        Exception: If metadata fetching fails
    """
    validate_youtube_video_id(video_id)

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise Exception(
            "YOUTUBE_API_KEY environment variable not set. Please obtain a YouTube Data API v3 key from Google Cloud Console and set the environment variable."
        )

    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if not data.get("items") or len(data["items"]) == 0:
            raise Exception(f"Video not found: {video_id}")

        video = data["items"][0]["snippet"]
        title = sanitize_title(video["title"])

        return {"title": title, "description": video["description"]}

    except requests.RequestException as e:
        raise Exception(f"Failed to get metadata: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to get metadata: {str(e)}")


def execute(args: dict[str, Any]) -> str:
    """Main tool entry point for OpenCode.

    Args:
        args: Dictionary containing tool arguments
            - video_id: YouTube video ID to fetch transcript and metadata for

    Returns:
        Filename of the written JSON file

    Raises:
        Exception: If tool execution fails
    """
    # Validate required environment variable
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise Exception(
            "YOUTUBE_API_KEY environment variable not set. Please obtain a YouTube Data API v3 key from Google Cloud Console and set the environment variable."
        )

    try:
        video_url = args.get("video_id")
        if not video_url:
            raise Exception("video_id argument is required")
        video_id = return_id(video_url)
        if not video_id:
            raise Exception("video_id argument is required")

        metadata = get_youtube_metadata(video_id)
        title = metadata["title"]
        description = metadata["description"]
        transcript = get_youtube_transcript(video_id)

        result = {
            "video_id": video_id,
            "title": title,
            "transcript": transcript,
            "description": description,
        }

        filename = f"{uuid.uuid4()}.json"
        with open(filename, "w") as f:
            json.dump(result, f)

        return filename

    except Exception as e:
        raise Exception(f"YouTube tool failed: {str(e)}")


# For direct testing
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run youtube_metadata.py <video_id>")
        sys.exit(1)

    try:
        result = execute({"video_id": return_id(sys.argv[1])})
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
