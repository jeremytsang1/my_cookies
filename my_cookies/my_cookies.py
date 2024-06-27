"""Retrieve leetcode cookies from Chrome with local keyring"""

import sys
from http.cookiejar import Cookie, CookieJar
from typing import Callable

import browser_cookie3


def main():
    """Print cookies."""

    browsers: dict[str, Callable] = {
        "Chrome": browser_cookie3.chrome,
        "Chromium": browser_cookie3.chromium,
        "Brave": browser_cookie3.brave,
        "Firefox": browser_cookie3.firefox,
        "Microsoft Edge": browser_cookie3.edge,
    }

    leetcode_cookies: list[Cookie] = []

    for item in browsers.items():
        leetcode_cookies = find_cookies(*item)
        if len(leetcode_cookies) == 2:  # Hardcoded. Same length as `cookie_names`.
            print_cookies(leetcode_cookies)
            return
    print(
        "get cookie failed, make sure you have Chrome, Chromium, Brave, Firefox or Edge installed and login in LeetCode with one of them at least once."
    )


def find_cookies(browser_name: str, cookiejar_function: Callable) -> list[Cookie]:
    leetcode_com: str = "leetcode.com"
    cookie_names: tuple[str, str] = ("LEETCODE_SESSION", "csrftoken")

    try:
        cookiejar: CookieJar = cookiejar_function(domain_name=leetcode_com)
    except Exception:
        print(f"get cookie from {browser_name} failed", file=sys.stderr)
        return []

    return list(filter(lambda cookie: cookie.name in cookie_names, cookiejar))


def print_cookies(leetcode_cookies: list[Cookie]) -> None:
    for c in leetcode_cookies:
        print(c.name, c.value)


if __name__ == "__main__":
    main()
