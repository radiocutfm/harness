# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Read Trello data as JSON without persisting credentials."""

from __future__ import annotations

import argparse
import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://api.trello.com/1"
RETRIES = 3


def credentials() -> dict[str, str]:
    """Return ephemeral credentials or fail without exposing their values."""
    key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_API_TOKEN")
    if not key or not token:
        raise SystemExit("Faltan TRELLO_API_KEY y/o TRELLO_API_TOKEN en el entorno.")
    return {"key": key, "token": token}


def get(path: str, params: dict[str, str], timeout: int) -> object:
    """Fetch JSON with bounded retries for transient Trello failures."""
    query = urlencode(credentials() | params)
    request = Request(f"{BASE_URL}{path}?{query}", headers={"Accept": "application/json"})
    for attempt in range(RETRIES):
        try:
            with urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt == RETRIES - 1:
                raise SystemExit(f"Trello respondió HTTP {error.code}; revisá permisos o intentá más tarde.") from None
            retry_after = error.headers.get("Retry-After")
            time.sleep(float(retry_after) if retry_after else 2**attempt)
        except URLError as error:
            if attempt == RETRIES - 1:
                raise SystemExit(f"No se pudo conectar con Trello: {error.reason}") from None
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def limit_items(payload: object, limit: int) -> object:
    """Bound collection responses without altering object-shaped responses."""
    return payload[:limit] if isinstance(payload, list) else payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=20)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("boards")
    board = subparsers.add_parser("board")
    board.add_argument("board_id")
    lists = subparsers.add_parser("lists")
    lists.add_argument("board_id")
    cards = subparsers.add_parser("cards")
    cards.add_argument("board_id")
    search = subparsers.add_parser("search")
    search.add_argument("query")
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 1000:
        parser.error("--limit debe estar entre 1 y 1000")

    routes = {
        "boards": ("/members/me/boards", {"fields": "id,name,url,closed"}),
        "board": (f"/boards/{args.board_id}", {"fields": "id,name,url,desc,closed,dateLastActivity"}),
        "lists": (f"/boards/{args.board_id}/lists", {"fields": "id,name,closed,pos"}),
        "cards": (f"/boards/{args.board_id}/cards", {"fields": "id,name,url,desc,idList,closed,dateLastActivity,due"}),
        "search": ("/search", {"query": args.query, "modelTypes": "cards,boards", "cards_limit": str(args.limit)}),
    }
    path, params = routes[args.command]
    print(json.dumps(limit_items(get(path, params, args.timeout), args.limit), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
