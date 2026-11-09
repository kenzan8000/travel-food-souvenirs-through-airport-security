#!/usr/bin/env python3
"""Render a food souvenir list (carry-on safe, allowed at the destination) from JSON to Markdown.

Checks each item's image candidates in order and keeps the first one that loads
as an image, rewrites it to a GitHub image proxy URL so chat apps that only trust
a few image hosts show it, drops items that fail the carry-on or customs checks,
and prints Markdown for the chat. Warnings go to stderr.

Usage:
    python3 scripts/render_souvenirs.py list.json
    python3 scripts/render_souvenirs.py list.json -o list.md --no-check-images
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import sys
import urllib.error
import urllib.request

USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
)
IMAGE_REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "image/webp,image/png,image/jpeg,image/*;q=0.8",
    "Referer": "https://example.com/",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
}
EMBEDDABLE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_IMAGE_BYTES = 1_500_000
GITHUB_MARKDOWN_API = "https://api.github.com/markdown"
CUSTOMS_STATUSES = ("allowed", "declare", "banned")

DEFAULT_LABELS = {
    "travel_rules": "Travel rules",
    "souvenirs": "Souvenirs",
    "left_out": "Left out",
    "sources": "Sources",
    "rejected_sources": "Rejected sources",
    "carry_on_ok": "carry-on OK",
    "status_allowed": "allowed",
    "status_declare": "declare at customs",
    "status_banned": "banned",
    "official": "official",
    "size": "Size",
    "carry_on": "Carry-on",
    "customs": "Customs",
    "shelf_life": "Shelf life",
    "packing": "Packing",
    "where_to_buy": "Where to buy",
    "made_from": "Made from",
    "how_made": "How it's made",
    "taste": "Taste",
    "look_for": "Look for on the label",
    "examples": "Examples",
    "tips": "From the sources",
    "local_terms": "Local terms",
    "item_sources": "Sources",
}


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def md_url(url: str) -> str:
    return url.replace(" ", "%20").replace("(", "%28").replace(")", "%29")


def sniff_image(head: bytes) -> bool:
    return (
        head.startswith(b"\xff\xd8\xff")
        or head.startswith(b"\x89PNG\r\n\x1a\n")
        or head.startswith((b"GIF87a", b"GIF89a"))
        or (head[:4] == b"RIFF" and head[8:12] == b"WEBP")
    )


def check_image(url: str, timeout: float) -> tuple[str, str, str]:
    """Return (result, final_url, reason). result is "ok", "bad" or "unreachable".

    The request imitates a chat app embedding the image from another site, so images
    that only load on their own site (hotlink protection, Cross-Origin-Resource-Policy)
    are rejected. The final URL after redirects is returned, because some chat apps do
    not follow redirects for embedded images.
    """
    if not url.startswith("https://"):
        return "bad", url, "not https (many chat apps block http images)"
    request = urllib.request.Request(md_url(url), headers=IMAGE_REQUEST_HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
            corp = response.headers.get("Cross-Origin-Resource-Policy", "").strip().lower()
            length = response.headers.get("Content-Length", "")
            if not final_url.startswith("https://"):
                return "bad", final_url, "redirects to http"
            if content_type not in EMBEDDABLE_TYPES:
                return "bad", final_url, f"content type {content_type or 'missing'}"
            if corp in ("same-origin", "same-site"):
                return "bad", final_url, f"Cross-Origin-Resource-Policy: {corp}"
            if length.isdigit() and int(length) > MAX_IMAGE_BYTES:
                return "bad", final_url, f"too large ({int(length) // 1024} KB); use a smaller thumbnail"
            if not sniff_image(response.read(16)):
                return "bad", final_url, "body is not an image"
            return "ok", final_url, ""
    except urllib.error.HTTPError as error:
        return "bad", url, f"HTTP {error.code}"
    except ValueError as error:
        return "bad", url, str(error)
    except (urllib.error.URLError, TimeoutError, OSError):
        return "unreachable", url, "could not be reached"


def github_proxy_url(url: str, timeout: float) -> str | None:
    """Return GitHub's camo proxy URL for an image, or None if GitHub can't be reached.

    Some chat apps, often on mobile and web, only load images from an allowlist of
    hosts, and camo.githubusercontent.com is commonly on it. GitHub's Markdown API
    rewrites image URLs to signed camo URLs without uploading anything.
    """
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "travel-food-souvenirs-through-airport-security"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps({"text": f"![]({md_url(url)})", "mode": "gfm"}).encode()
    request = urllib.request.Request(GITHUB_MARKDOWN_API, data=body, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            html = response.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        warn(f"GitHub Markdown API failed ({error}); photos may not show in apps that only trust a few image hosts")
        return None
    match = re.search(r'<img src="(https://camo\.githubusercontent\.com/[^"]+)"', html)
    return match.group(1) if match else None


def choose_images(items: list[dict], check: bool, proxy: bool, timeout: float) -> dict[str, str | None]:
    chosen: dict[str, str | None] = {}
    if not check:
        for item in items:
            images = item.get("images") or []
            chosen[item["id"]] = images[0] if images else None
        return chosen

    def first_working(item: dict) -> tuple[str | None, list[str]]:
        results = []
        for url in item.get("images") or []:
            result, final_url, reason = check_image(url, timeout)
            results.append(result)
            if result != "ok":
                warn(f"{item['id']}: image rejected ({reason}): {url}")
                continue
            if not proxy:
                return final_url, results
            camo_url = github_proxy_url(final_url, timeout)
            if camo_url is None:
                return final_url, results
            camo_result, _, camo_reason = check_image(camo_url, timeout)
            if camo_result == "ok":
                return camo_url, results
            warn(f"{item['id']}: GitHub's image proxy can't load it ({camo_reason}): {url}")
        return None, results

    all_results: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for item, (url, results) in zip(items, pool.map(first_working, items)):
            chosen[item["id"]] = url
            all_results += results
    if all_results and all(r == "unreachable" for r in all_results):
        warn(
            "no image could be reached; this environment may have no network access. "
            "Check the image URLs with your own browsing tool, keep only working ones, "
            "and rerun with --no-check-images."
        )
    return chosen


def terms_text(terms: list[dict]) -> str:
    out = []
    for term in terms:
        text = f"*{term.get('term', '')}* = {term.get('meaning', '')}"
        if term.get("pronunciation"):
            text += f" ({term['pronunciation']})"
        out.append(text)
    return "; ".join(out)


def size_text(item: dict) -> str:
    return " ".join(x for x in (item.get("pack_size"), item.get("price")) if x)


def group_by_category(items: list[dict]) -> list[tuple[str, list[dict]]]:
    groups: dict[str, list[dict]] = {}
    for item in items:
        groups.setdefault(item.get("category") or "", []).append(item)
    return list(groups.items())


def render_overview(groups: list[tuple[str, list[dict]]], labels: dict) -> list[str]:
    lines: list[str] = []
    number = 0
    for category, items in groups:
        if category:
            lines += [f"**{category}**", ""]
        for item in items:
            number += 1
            parts = [
                item.get("type", ""),
                size_text(item),
                labels["carry_on_ok"],
                labels[f"status_{item['customs']['status']}"],
            ]
            summary = " · ".join(x for x in parts if x)
            lines.append(f"{number}. **{item['name']}**: {summary}")
        lines.append("")
    return lines


def render_card(item: dict, image: str | None, source_numbers: dict[str, int], labels: dict) -> list[str]:
    lines = [f"### {item['name']}", ""]
    alt = item.get("local_name") or item["name"]
    if image:
        lines += [f"![{alt}]({md_url(image)})", ""]
    else:
        warn(f"{item['id']}: no working image; find one (see Photos in SKILL.md) and rerun")

    maker = item.get("producer") or item.get("maker")
    summary = [item.get("type", ""), ", ".join(x for x in (maker, item.get("origin")) if x)]
    summary_text = " · ".join(x for x in summary if x)
    if summary_text:
        lines += [f"*{summary_text}*", ""]

    bullets: list[tuple[str, str]] = []
    if size_text(item):
        bullets.append((labels["size"], size_text(item)))
    bullets.append((labels["carry_on"], str(item["carry_on"])))

    customs = item["customs"]
    customs_text = labels[f"status_{customs['status']}"]
    if customs.get("note"):
        customs_text += f". {customs['note']}"
    if customs.get("source"):
        customs_text += f" [{labels['official']}]({md_url(customs['source'])})"
    bullets.append((labels["customs"], customs_text))

    for key, label in (("shelf_life", "shelf_life"), ("packing_tips", "packing"), ("where_to_buy", "where_to_buy"),
                       ("made_from", "made_from"), ("how_made", "how_made"), ("taste", "taste")):
        if item.get(key):
            bullets.append((labels[label], str(item[key])))

    if item.get("label_hints"):
        bullets.append((labels["look_for"], terms_text(item["label_hints"])))
    if item.get("examples"):
        bullets.append((labels["examples"], ", ".join(item["examples"])))
    if item.get("tips"):
        bullets.append((labels["tips"], str(item["tips"])))
    if item.get("local_terms"):
        bullets.append((labels["local_terms"], terms_text(item["local_terms"])))

    refs = [f"[{source_numbers[url]}]({md_url(url)})" for url in item.get("sources") or [] if url in source_numbers]
    if refs:
        bullets.append((labels["item_sources"], " ".join(refs)))

    lines += [f"- **{label}:** {text}" for label, text in bullets]
    lines.append("")
    return lines


def keep_items(items: list[dict], used_urls: set[str], left_out: list[dict]) -> list[dict]:
    """Return the items that pass every check; banned items are appended to left_out."""
    kept = []
    seen_ids = set()
    left_out_names = {entry.get("name") for entry in left_out}
    for index, item in enumerate(items):
        if not item.get("id") or not item.get("name"):
            warn(f"souvenirs[{index}]: missing id or name, left out")
            continue
        if item["id"] in seen_ids:
            warn(f"{item['id']}: duplicate id, left out")
            continue
        if not any(url in used_urls for url in item.get("sources") or []):
            warn(f"{item['id']}: no used source, left out")
            continue
        if not item.get("carry_on"):
            warn(f"{item['id']}: no carry_on reason, left out")
            continue
        customs = item.get("customs")
        status = customs.get("status") if isinstance(customs, dict) else None
        if status not in CUSTOMS_STATUSES:
            warn(f"{item['id']}: customs.status missing or not one of {', '.join(CUSTOMS_STATUSES)}, left out")
            continue
        if status == "banned":
            warn(f"{item['id']}: banned at the destination, moved to left_out")
            if item["name"] not in left_out_names:
                left_out.append({"name": item["name"], "reason": customs.get("note", ""), "sources": item.get("sources", [])})
            continue
        seen_ids.add(item["id"])
        kept.append(item)
    return kept


def render_left_out(left_out: list[dict], source_numbers: dict[str, int]) -> list[str]:
    lines = []
    for entry in left_out:
        text = f"- **{entry.get('name', '')}**"
        if entry.get("reason"):
            text += f": {entry['reason']}"
        refs = [f"[{source_numbers[url]}]({md_url(url)})" for url in entry.get("sources") or [] if url in source_numbers]
        if refs:
            text += " " + " ".join(refs)
        lines.append(text)
    return lines


def render(data: dict, check_images: bool, proxy_images: bool, timeout: float) -> str:
    labels = {**DEFAULT_LABELS, **(data.get("labels") or {})}
    sources = data.get("sources") or []
    used = [s for s in sources if s.get("status") == "used" and s.get("url")]
    rejected = [s for s in sources if s.get("status") == "rejected"]
    source_numbers = {s["url"]: i for i, s in enumerate(used, start=1)}

    left_out = list(data.get("left_out") or [])
    souvenirs = keep_items(data.get("souvenirs") or [], set(source_numbers), left_out)
    groups = group_by_category(souvenirs)
    images = choose_images(souvenirs, check_images, proxy_images, timeout)

    out: list[str] = []

    if data.get("travel_rules"):
        out += [f"## {labels['travel_rules']}", ""]
        out += [f"- {rule}" for rule in data["travel_rules"]]
        out.append("")

    if souvenirs:
        out += [f"## {labels['souvenirs']}", ""]
        out += render_overview(groups, labels)
        for _, items in groups:
            for item in items:
                out += render_card(item, images.get(item["id"]), source_numbers, labels)

    if left_out:
        out += [f"## {labels['left_out']}", ""]
        out += render_left_out(left_out, source_numbers)
        out.append("")

    if used:
        out += [f"## {labels['sources']}", ""]
        for number, source in enumerate(used, start=1):
            details = ", ".join(str(source[k]) for k in ("author", "date", "kind") if source.get(k))
            text = f"{number}. [{source.get('title') or source['url']}]({md_url(source['url'])})"
            if details:
                text += f": {details}"
            out.append(text)
        out.append("")

    if rejected:
        out += [f"### {labels['rejected_sources']}", ""]
        for source in rejected:
            title = source.get("title") or source.get("url", "")
            link = f"[{title}]({md_url(source['url'])})" if source.get("url") else title
            out.append(f"- {link}: {source.get('reason', '')}")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="souvenir list JSON")
    parser.add_argument("-o", "--output", help="write Markdown here instead of stdout")
    parser.add_argument("--no-check-images", action="store_true", help="use the first image candidate unchecked")
    parser.add_argument(
        "--no-proxy", action="store_true",
        help="output original image URLs instead of GitHub proxy URLs (photos may then not show in apps that only trust a few image hosts)",
    )
    parser.add_argument("--timeout", type=float, default=8.0, help="seconds per image request (default 8)")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    markdown = render(data, not args.no_check_images, not args.no_proxy, args.timeout)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
