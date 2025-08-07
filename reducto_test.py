"""Utilities to parse PDFs via Reducto API.

This script mirrors the original notebook but organizes the code into
reusable functions for easier maintenance and testing.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from reducto import Reducto, ReductoError


OPTIONS = {
    "ocr_mode": "agentic",
    "extraction_mode": "ocr",
    "chunking": {"chunk_mode": "variable"},
}

ADVANCED_OPTIONS = {
    "ocr_system": "multilingual",
    "page_range": {"start": 1, "end": 10},
    "table_output_format": "ai_json",
    "merge_tables": True,
}

EXPERIMENTAL_OPTIONS = {
    "enable_checkboxes": True,
    "return_figure_images": False,
    "rotate_pages": True,
}


def create_client() -> Reducto:
    """Create a Reducto client using an API key from the environment."""
    load_dotenv()
    api_key = os.getenv("REDUCTO_API_KEY")
    if not api_key:
        raise ReductoError(
            "REDUCTO_API_KEY is not set. Provide it via environment variable or .env file."
        )
    return Reducto(api_key=api_key)


def parse_document(client: Reducto, file_path: Path) -> dict:
    """Upload and parse a document, returning the parsed data."""
    upload = client.upload(file=file_path)
    result = client.parse.run(
        document_url=upload,
        options=OPTIONS,
        advanced_options=ADVANCED_OPTIONS,
        experimental_options=EXPERIMENTAL_OPTIONS,
    )
    return result.model_dump()


def save_parsed_data(data: dict, out_path: Path) -> None:
    """Write parsed data to a JSON file."""
    with out_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def extract_page_blocks(parsed: dict, page_number: int) -> Iterable[str]:
    """Yield text blocks for a specific page from parsed data."""
    for chunk in parsed.get("result", {}).get("chunks", []):
        for block in chunk.get("blocks", []):
            if block.get("bbox", {}).get("page") == page_number:
                content = block.get("content")
                if content is not None:
                    yield content


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Parse a PDF using Reducto")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("sample.pdf"),
        help="Path to the PDF file to parse",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("parsed_data.json"),
        help="Where to write parsed JSON data",
    )
    parser.add_argument(
        "--page",
        type=int,
        default=6,
        help="Page number for block extraction",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client()
    parsed = parse_document(client, args.input)
    save_parsed_data(parsed, args.output)

    for block in extract_page_blocks(parsed, page_number=args.page):
        print(block)


if __name__ == "__main__":
    main()
