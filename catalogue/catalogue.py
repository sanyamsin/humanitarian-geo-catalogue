"""
catalogue/catalogue.py
=======================
Core catalogue engine — CRUD operations, search, and discovery.
Stores metadata records as JSON files locally.
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

from catalogue.metadata import MetadataRecord, validate_record
import yaml


# ── CATALOGUE ENGINE ──────────────────────────────────────────

class GeoCatalogue:
    """
    Local geospatial data catalogue.
    Records stored as JSON files in data/sample_records/.
    """

    def __init__(self, config_path: str = "config/catalogue.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.records_path = Path(
            self.config["catalogue"]["storage"]["records_path"]
            if "storage" in self.config["catalogue"]
            else "data/sample_records"
        )
        self.records_path.mkdir(parents=True, exist_ok=True)

    # ── CRUD ─────────────────────────────────────────────────

    def add_record(self, record: MetadataRecord) -> dict:
        """Validates and saves a metadata record."""
        errors = validate_record(record)
        if errors:
            return {"success": False, "errors": errors}

        record.date_modified = datetime.utcnow().date().isoformat()
        file_path = self.records_path / f"{record.record_id}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record.to_dict(), f, indent=2, ensure_ascii=False)

        return {"success": True, "record_id": record.record_id}

    def get_record(self, record_id: str) -> Optional[dict]:
        """Returns a single record by ID."""
        file_path = self.records_path / f"{record_id}.json"
        if not file_path.exists():
            return None
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)

    def list_records(self) -> List[dict]:
        """Returns all records in the catalogue."""
        records = []
        for file_path in sorted(self.records_path.glob("*.json")):
            with open(file_path, encoding="utf-8") as f:
                records.append(json.load(f))
        return records

    def delete_record(self, record_id: str) -> bool:
        """Deletes a record by ID."""
        file_path = self.records_path / f"{record_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    # ── SEARCH ───────────────────────────────────────────────

    def search(
        self,
        query: str = "",
        domain: str = "",
        classification: str = "",
        topic_category: str = "",
        geometry_type: str = "",
    ) -> List[dict]:
        """
        Searches records by keyword, domain, classification,
        topic category, and geometry type.
        """
        records = self.list_records()
        results = []

        for r in records:
            # Keyword search across title, abstract, keywords
            if query:
                searchable = " ".join([
                    r.get("title", ""),
                    r.get("abstract", ""),
                    " ".join(r.get("keywords", [])),
                    r.get("source_organization", ""),
                ]).lower()
                if query.lower() not in searchable:
                    continue

            if domain and r.get("domain") != domain:
                continue

            if classification and r.get("classification") != classification:
                continue

            if topic_category and r.get("topic_category") != topic_category:
                continue

            if geometry_type and r.get("geometry_type") != geometry_type:
                continue

            results.append(r)

        return results

    # ── STATS ─────────────────────────────────────────────────

    def stats(self) -> dict:
        """Returns catalogue statistics."""
        records = self.list_records()
        if not records:
            return {"total": 0}

        domains = {}
        classifications = {}
        formats = {}

        for r in records:
            d = r.get("domain", "Unknown")
            domains[d] = domains.get(d, 0) + 1

            c = r.get("classification", "Unknown")
            classifications[c] = classifications.get(c, 0) + 1

            fmt = r.get("format", "Unknown")
            formats[fmt] = formats.get(fmt, 0) + 1

        return {
            "total": len(records),
            "by_domain": domains,
            "by_classification": classifications,
            "by_format": formats,
        }