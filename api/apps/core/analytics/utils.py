"""
Bot / crawler detection utilities for analytics.

Checks user-agent strings against known bot patterns and provides
helper functions to filter out non-human traffic.
"""

import re
from typing import Optional

# ── Known bot / crawler patterns ──────────────────────────────────────────
# These are matched case-insensitively against the user-agent string.

_BOT_PATTERNS: list[str] = [
    # Search engine crawlers
    "googlebot", "adsbot-google", "mediapartners-google",
    "bingbot", "msnbot", "adidxbot", "bingpreview",
    "slurp",  # Yahoo
    "duckduckbot",
    "baiduspider",
    "yandexbot", "yandex.com/bots",
    "sogou", "sogou web spider",
    "exabot",
    "facebot", "facebookexternalhit",
    "twitterbot",
    "linkedinbot",
    "whatsapp",
    "telegrambot",
    "discordbot",
    "slackbot",
    "pinterest",
    "redditbot",
    "tumblr",
    "outbrain",
    "embedly",

    # SEO / monitoring tools
    "ahrefsbot", "ahrefssitemap",
    "semrushbot", "semrush",
    "majestic", "mj12bot",
    "rogerbot",  # Moz
    "dotbot",  # Moz
    "screaming frog",
    "sitebulb",
    "deepcrawl",
    "oncrawl",
    "amperity",

    # Generic crawlers
    "crawler", "spider", "scraper", "bot/", "bot.",
    "python-urllib", "python-requests",
    "go-http-client", "go-http",
    "java/", "jakarta commons",
    "apache-httpclient",
    "httpclient", "http client",
    "wget", "curl", "libwww",
    "lwp-trivial", "lwp::simple",
    "phpcrawl", "php crawl",
    "node-fetch", "got/", "axios",
    "insomnia", "postmanruntime",
    "okkaido",  # headless browser
    "panscient",

    # Headless / automation browsers
    "headless", "headlesschrome",
    "phantomjs", "phantom",
    "selenium", "webdriver",
    "puppeteer", "playwright",
    "cypress",
    "electron",
    "nightmare",

    # Monitoring / health checks
    "uptimerobot", "pingdom",
    "statuscake", "site24x7",
    "monitis", "newrelic",
    "datadog",
    "hetrixtools",
    "checkly",
    "better uptime",
    "freshping",
    "gtmetrix",
    "pagespeed", "lighthouse",

    # Security scanners
    "nessus", "nikto", "acunetix",
    "burpsuite", "netsparker",
    "qualys", "openvas",
    "zap",  # OWASP ZAP
    "masscan", "nmap",

    # Known bot signatures
    "bytespider",  # ByteDance/TikTok
    "petalbot",  # Huawei
    "seznambot",
    "qwantify",
    "yisouspider",
    "daumoa",
    "naverbot",
    "coccocbot",
    "moatbot",
    "criteo",
    "iaspetspider",
    "admantx",
    "grapeshot",
    "taboola",
    "revcontent",
    "zemanta",

    # Empty or obviously fake
    "-",  # often used by bots with minimal UA
]

# Pre-compile patterns into a single regex for efficiency
_BOT_RE = re.compile(
    "|".join(re.escape(p) for p in _BOT_PATTERNS),
    re.IGNORECASE,
)

# Minimal/suspicious user-agent length threshold
_MIN_UA_LENGTH = 8


def is_bot(user_agent: Optional[str]) -> bool:
    """Return True if the user-agent string matches a known bot/crawler pattern.

    Also flags empty, None, or very short user-agent strings as bots.
    """
    if not user_agent or not user_agent.strip():
        return True

    ua = user_agent.strip()

    # Very short user-agents are almost always bots or scripts
    if len(ua) < _MIN_UA_LENGTH:
        return True

    return bool(_BOT_RE.search(ua))


def is_bot_request(request) -> bool:
    """Check a DRF request object for bot signals.

    Examines both the JSON payload's ``user_agent`` field and the
    actual HTTP ``User-Agent`` header.
    """
    # Check the user_agent in the request payload
    ua = (request.data or {}).get("user_agent", "")
    if is_bot(ua):
        return True

    # Also check the actual HTTP header (server-side UA)
    http_ua = request.META.get("HTTP_USER_AGENT", "")
    if is_bot(http_ua):
        return True

    return False
