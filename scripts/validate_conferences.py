#!/usr/bin/env python3
"""Validate the conference records used by the Jekyll site."""

from __future__ import annotations

import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

try:
    import yaml
except ImportError as exc:  # pragma: no cover - depends on the local environment
    raise SystemExit("PyYAML is required: install it with `python3 -m pip install PyYAML`.") from exc


DATA_FILE = Path(__file__).resolve().parents[1] / "_data" / "conferences.yml"
ALLOWED_CATEGORIES = {"XR", "HRI", "ROB"}
REQUIRED_FIELDS = {
    "title",
    "year",
    "id",
    "full_name",
    "link",
    "deadline",
    "place",
    "date",
    "start",
    "end",
    "sub",
}
DEADLINE_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
ID_RE = re.compile(r"^[a-z0-9]+$")
AMBIGUOUS_TIMEZONES = {
    "PST",
    "PDT",
    "MST",
    "MDT",
    "CST",
    "CDT",
    "EST",
    "EDT",
    "BST",
    "KST",
    "JST",
    "AEST",
    "AEDT",
}


def parse_iso_date(value: object, field: str, label: str, errors: list[str]) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{label}: {field} must be a quoted ISO date (YYYY-MM-DD)")
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label}: {field} is not a valid ISO date: {value!r}")
        return None
    if parsed.isoformat() != value:
        errors.append(f"{label}: {field} must be zero-padded: {value!r}")
    return parsed


def validate_deadline(value: object, field: str, label: str, errors: list[str]) -> bool:
    if value == "TBA":
        return False
    if not isinstance(value, str) or not DEADLINE_RE.fullmatch(value):
        errors.append(f"{label}: {field} must be 'TBA' or YYYY-MM-DD HH:MM:SS")
        return True
    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        errors.append(f"{label}: {field} is not a real calendar date/time: {value!r}")
    return True


def validate_timezone(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label}: timezone is required for an announced deadline")
        return
    if value == "UTC-12":
        return
    if value in AMBIGUOUS_TIMEZONES or re.fullmatch(r"(?:GMT|UTC)[+-]\d{1,2}", value):
        errors.append(f"{label}: ambiguous timezone {value!r}; use an IANA name or UTC-12 for AoE")
        return
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError):
        errors.append(f"{label}: invalid IANA timezone {value!r}")


def main() -> int:
    try:
        records = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"Could not load {DATA_FILE}: {exc}", file=sys.stderr)
        return 2

    if not isinstance(records, list):
        print(f"{DATA_FILE}: top-level YAML value must be a list", file=sys.stderr)
        return 1

    errors: list[str] = []
    ids: list[str] = []
    editions: list[tuple[str, int]] = []

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"record {index}: expected a mapping")
            continue

        label = str(record.get("id") or f"record {index}")
        missing = sorted(field for field in REQUIRED_FIELDS if field not in record)
        if missing:
            errors.append(f"{label}: missing required fields: {', '.join(missing)}")

        conf_id = record.get("id")
        if isinstance(conf_id, str):
            ids.append(conf_id)
            if not ID_RE.fullmatch(conf_id):
                errors.append(f"{label}: id must contain only lowercase letters and digits")
        else:
            errors.append(f"{label}: id must be a string")

        year = record.get("year")
        if not isinstance(year, int) or isinstance(year, bool):
            errors.append(f"{label}: year must be numeric")

        title = record.get("title")
        if isinstance(title, str) and isinstance(year, int):
            editions.append((title.casefold().strip(), year))

        categories = record.get("sub")
        if not isinstance(categories, list) or not categories:
            errors.append(f"{label}: sub must be a non-empty YAML list")
        else:
            invalid = [category for category in categories if category not in ALLOWED_CATEGORIES]
            if invalid:
                errors.append(f"{label}: invalid categories: {', '.join(map(str, invalid))}")
            if len(categories) != len(set(categories)):
                errors.append(f"{label}: sub contains duplicate categories")

        url = record.get("link")
        if not isinstance(url, str):
            errors.append(f"{label}: link must be a URL string")
        else:
            parsed_url = urlparse(url)
            if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
                errors.append(f"{label}: malformed URL: {url!r}")

        start = parse_iso_date(record.get("start"), "start", label, errors)
        end = parse_iso_date(record.get("end"), "end", label, errors)
        if start and end:
            if start > end:
                errors.append(f"{label}: start date must not be after end date")
            if isinstance(year, int) and (start.year != year or end.year != year):
                errors.append(f"{label}: event dates must match conference year {year}")

        has_timed_deadline = validate_deadline(record.get("deadline"), "deadline", label, errors)
        if "abstract_deadline" in record:
            has_timed_deadline |= validate_deadline(
                record["abstract_deadline"], "abstract_deadline", label, errors
            )
        if has_timed_deadline:
            validate_timezone(record.get("timezone"), label, errors)
        elif "timezone" in record:
            validate_timezone(record.get("timezone"), label, errors)

    duplicate_ids = [value for value, count in Counter(ids).items() if count > 1]
    if duplicate_ids:
        errors.append(f"duplicate conference IDs: {', '.join(sorted(duplicate_ids))}")

    duplicate_editions = [
        f"{title} {year}" for (title, year), count in Counter(editions).items() if count > 1
    ]
    if duplicate_editions:
        errors.append(f"duplicate conference editions: {', '.join(sorted(duplicate_editions))}")

    if errors:
        print(f"Conference validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(records)} conference records in {DATA_FILE}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
