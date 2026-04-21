"""
catalogue/metadata.py
======================
ISO 19115:2014 metadata schema for humanitarian geospatial datasets.
Defines the MetadataRecord dataclass and validation logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import json
import uuid


# ── METADATA RECORD ───────────────────────────────────────────

@dataclass
class MetadataRecord:
    """
    Geospatial dataset metadata record.
    Aligned with ISO 19115:2014.
    """

    # Mandatory fields
    title: str
    abstract: str
    domain: str
    classification: str
    geometry_type: str
    coordinate_reference_system: str
    source_organization: str
    data_steward: str
    update_frequency: str
    format: str

    # Auto-generated
    record_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    date_created: str = field(default_factory=lambda: datetime.utcnow().date().isoformat())
    date_modified: str = field(default_factory=lambda: datetime.utcnow().date().isoformat())

    # Optional fields
    keywords: List[str] = field(default_factory=list)
    topic_category: str = ""
    bounding_box: dict = field(default_factory=dict)
    temporal_extent_start: str = ""
    temporal_extent_end: str = ""
    source_url: str = ""
    licence: str = ""
    lineage_description: str = ""
    known_issues: str = ""
    access_url: str = ""
    language: str = "fr"

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "title": self.title,
            "abstract": self.abstract,
            "domain": self.domain,
            "classification": self.classification,
            "geometry_type": self.geometry_type,
            "crs": self.coordinate_reference_system,
            "source_organization": self.source_organization,
            "data_steward": self.data_steward,
            "update_frequency": self.update_frequency,
            "format": self.format,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "keywords": self.keywords,
            "topic_category": self.topic_category,
            "bounding_box": self.bounding_box,
            "temporal_extent_start": self.temporal_extent_start,
            "temporal_extent_end": self.temporal_extent_end,
            "source_url": self.source_url,
            "licence": self.licence,
            "lineage_description": self.lineage_description,
            "known_issues": self.known_issues,
            "access_url": self.access_url,
            "language": self.language,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


# ── VALIDATION ────────────────────────────────────────────────

VALID_DOMAINS = ["DD01", "DD02", "DD03", "DD04", "DD05"]
VALID_CLASSIFICATIONS = ["Public", "Restricted", "Confidential", "Sensitive"]
VALID_GEOMETRY_TYPES = ["Point", "LineString", "Polygon", "MultiPolygon", "Raster", "Mixed"]
VALID_FREQUENCIES = ["real-time", "daily", "weekly", "monthly", "quarterly", "annual", "irregular"]


def validate_record(record: MetadataRecord) -> List[str]:
    """
    Validates a MetadataRecord against ISO 19115 mandatory fields.
    Returns a list of error messages (empty = valid).
    """
    errors = []

    if not record.title or len(record.title.strip()) < 5:
        errors.append("Title is required and must be at least 5 characters.")

    if not record.abstract or len(record.abstract.strip()) < 20:
        errors.append("Abstract is required and must be at least 20 characters.")

    if record.domain not in VALID_DOMAINS:
        errors.append(f"Domain must be one of: {VALID_DOMAINS}")

    if record.classification not in VALID_CLASSIFICATIONS:
        errors.append(f"Classification must be one of: {VALID_CLASSIFICATIONS}")

    if record.geometry_type not in VALID_GEOMETRY_TYPES:
        errors.append(f"Geometry type must be one of: {VALID_GEOMETRY_TYPES}")

    if not record.coordinate_reference_system.startswith("EPSG:"):
        errors.append("CRS must be in EPSG format (e.g. EPSG:4326).")

    if not record.source_organization:
        errors.append("Source organization is required.")

    if not record.data_steward:
        errors.append("Data steward is required.")

    if record.update_frequency not in VALID_FREQUENCIES:
        errors.append(f"Update frequency must be one of: {VALID_FREQUENCIES}")

    return errors