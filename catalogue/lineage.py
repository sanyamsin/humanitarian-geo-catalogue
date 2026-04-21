"""
catalogue/lineage.py
=====================
Data lineage tracking - traces the origin and transformations
of geospatial datasets throughout their lifecycle.
Aligned with DAMA-DMBOK v2 Chapter 11.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional


# ── LINEAGE EVENT ─────────────────────────────────────────────

@dataclass
class LineageEvent:
    """
    A single transformation or processing step in a dataset's lineage.
    """
    event_type: str        # acquisition | transformation | validation | publication
    description: str
    performed_by: str
    tool_used: str = ""
    source_datasets: List[str] = field(default_factory=list)
    output_dataset: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type,
            "description": self.description,
            "performed_by": self.performed_by,
            "tool_used": self.tool_used,
            "source_datasets": self.source_datasets,
            "output_dataset": self.output_dataset,
            "timestamp": self.timestamp,
            "notes": self.notes,
        }


# ── LINEAGE RECORD ────────────────────────────────────────────

@dataclass
class LineageRecord:
    """
    Full lineage history for a single dataset.
    """
    record_id: str
    dataset_title: str
    events: List[LineageEvent] = field(default_factory=list)

    def add_event(self, event: LineageEvent):
        self.events.append(event)

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "dataset_title": self.dataset_title,
            "events": [e.to_dict() for e in self.events],
            "last_updated": datetime.utcnow().isoformat(),
        }


# ── LINEAGE STORE ─────────────────────────────────────────────

class LineageStore:
    """
    Stores and retrieves lineage records as JSON files.
    """

    def __init__(self, storage_path: str = "data/lineage"):
        self.path = Path(storage_path)
        self.path.mkdir(parents=True, exist_ok=True)

    def save(self, lineage: LineageRecord) -> bool:
        file_path = self.path / f"{lineage.record_id}_lineage.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(lineage.to_dict(), f, indent=2, ensure_ascii=False)
        return True

    def load(self, record_id: str) -> Optional[dict]:
        file_path = self.path / f"{record_id}_lineage.json"
        if not file_path.exists():
            return None
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)

    def list_all(self) -> List[dict]:
        records = []
        for file_path in sorted(self.path.glob("*_lineage.json")):
            with open(file_path, encoding="utf-8") as f:
                records.append(json.load(f))
        return records


# ── SAMPLE LINEAGE GENERATOR ──────────────────────────────────

def create_sample_lineage(record_id: str, title: str) -> LineageRecord:
    """Creates a realistic sample lineage for demo purposes."""
    lineage = LineageRecord(record_id=record_id, dataset_title=title)

    lineage.add_event(LineageEvent(
        event_type="acquisition",
        description="Dataset downloaded from OCHA HDX portal",
        performed_by="GIS Data Steward",
        tool_used="HDX CKAN API",
        source_datasets=["https://data.humdata.org"],
        output_dataset=record_id,
        notes="Original format: Shapefile ZIP"
    ))

    lineage.add_event(LineageEvent(
        event_type="transformation",
        description="Converted to GeoPackage, reprojected to EPSG:4326",
        performed_by="GIS Data Steward",
        tool_used="Python / GeoPandas / GDAL",
        source_datasets=[record_id],
        output_dataset=record_id,
        notes="Original CRS: EPSG:32632"
    ))

    lineage.add_event(LineageEvent(
        event_type="validation",
        description="Automated quality checks passed (15 checks, score 0.91)",
        performed_by="geodata-quality-pipeline",
        tool_used="geodata-quality-pipeline v1.0",
        source_datasets=[record_id],
        output_dataset=record_id,
        notes="2 warnings: duplicate name values"
    ))

    lineage.add_event(LineageEvent(
        event_type="publication",
        description="Published to humanitarian geo-catalogue",
        performed_by="GIS Data Governance Specialist",
        tool_used="humanitarian-geo-catalogue v1.0",
        source_datasets=[record_id],
        output_dataset=record_id,
        notes="Classification: Public"
    ))

    return lineage