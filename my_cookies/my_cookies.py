"""Retrieve leetcode cookies from Chrome with local keyring"""

import sys
from http.cookiejar import Cookie, CookieJar
from typing import Callable

import browser_cookie3


def main():
    """Print cookies."""
    leetcode_com: str = "leetcode.com"
    cookie_names: tuple[str, ...] = ("LEETCODE_SESSION", "csrftoken")
    browsers: dict[str, Callable] = {
        "Chrome": browser_cookie3.chrome,
        "Chromium": browser_cookie3.chromium,
        "Brave": browser_cookie3.brave,
        "Firefox": browser_cookie3.firefox,
        "Microsoft Edge": browser_cookie3.edge,
    }

    leetcode_cookies: list[Cookie] = []

    for browser_name, cookiejar_function in browsers.items():
        leetcode_cookies = find_cookies(
            leetcode_com, cookie_names, browser_name, cookiejar_function
        )
        if leetcode_cookies:
            print_cookies(leetcode_cookies, browser_name)
            return

    print(
        "get cookie failed, make sure you have Chrome, Chromium, Brave, Firefox or Edge installed and login in LeetCode with one of them at least once."
    )


def find_cookies(
    domain_name: str,
    cookie_names: tuple[str, ...],
    browser_name: str,
    cookiejar_function: Callable,
) -> list[Cookie]:
    ERROR_COOKIEJAR_FUNCTION: str = "get cookie from {} failed"
    ERROR_COOKIE_COUNT: str = "{} found invalid number of cookies: {}"

    try:
        cookiejar: CookieJar = cookiejar_function(domain_name=domain_name)
    except Exception:
        print(ERROR_COOKIEJAR_FUNCTION.format(browser_name), file=sys.stderr)
        return []

    leetcode_cookies: list[Cookie] = list(
        filter(lambda cookie: cookie.name in cookie_names, cookiejar)
    )

    # Warn user if the cookie jar function succeeds but not return the expected number
    # of cookies. Return an empty list to reflect this failure to find the cookies.
    if len(leetcode_cookies) != len(cookie_names):
        print(ERROR_COOKIE_COUNT.format(browser_name, len(leetcode_cookies)))
        return []

    return leetcode_cookies


def print_cookies(leetcode_cookies: list[Cookie], browser_name: str) -> None:
    # Print browser in case user runs multiple browsers and wants to know which one the
    # cookies are actually coming from when troubleshooting.
    print(f"Found cookies from {browser_name}")
    for c in leetcode_cookies:
        print(c.name, c.value)


if __name__ == "__main__":
    main()
