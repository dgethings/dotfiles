"""
Takes in a string, expected to be a URL and returns the YouTube video ID
"""

import sys
from urllib.parse import urlparse, parse_qs


def return_id(url: str) -> str:
    yt_url = urlparse(url)

    if "youtube.com" in yt_url.netloc or "m.youtube.com" in yt_url.netloc:
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
    elif "youtu.be" in yt_url.netloc:
        return yt_url.path.lstrip("/").split("?")[0].split("&")[0]
    elif "youtube-nocookie.com" in yt_url.netloc:
        return yt_url.path.split("/")[-1].split("?")[0]

    return ""


if __name__ == "__main__":
    arg = sys.argv[1]
    print(return_id(arg))
