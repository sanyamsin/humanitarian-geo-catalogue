# humanitarian-geo-catalogue

**ISO 19115 geospatial data catalogue for humanitarian organizations**  
Metadata management - Lineage tracking - Dataset discovery - Streamlit UI

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![ISO 19115](https://img.shields.io/badge/standard-ISO%2019115-darkblue.svg)](https://www.iso.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

Humanitarian GIS teams manage dozens of geospatial datasets across multiple
domains - admin boundaries, health facilities, logistics routes, conflict data.
Without a structured catalogue, datasets become undiscoverable, metadata
inconsistent, and lineage untraceable.

This catalogue provides:

- **Dataset discovery** - search by keyword, domain, classification, geometry type
- **ISO 19115 metadata** - standardized records for every dataset
- **Lineage tracking** - full transformation history from acquisition to publication
- **Streamlit UI** - accessible to both technical and non-technical staff
- **DAMA-DMBOK v2 aligned** - covers Metadata Management (Ch.12) and Data Lineage (Ch.11)

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/sanyamsin/humanitarian-geo-catalogue.git
cd humanitarian-geo-catalogue
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
```

### 2. Populate with sample data

```bash
python data/sample_records.py
```

### 3. Launch the catalogue

```bash
streamlit run dashboard/app.py
```

Opens at `http://localhost:8501`.

---

## Repository Structure

humanitarian-geo-catalogue/
├── catalogue/
│   ├── metadata.py         ← ISO 19115 MetadataRecord schema + validation
│   ├── catalogue.py        ← CRUD, search, discovery engine
│   └── lineage.py          ← Lineage events and traceability
├── dashboard/
│   └── app.py              ← Streamlit UI (4 pages)
├── data/
│   ├── sample_records/     ← JSON metadata records
│   ├── lineage/            ← JSON lineage files
│   └── sample_records.py   ← Sample data generator
├── config/
│   └── catalogue.yaml      ← Catalogue configuration
├── requirements.txt
└── README.md

---

## Catalogue Pages

| Page | Description |
|------|-------------|
| Discover datasets | Search and filter all datasets by keyword, domain, classification |
| Add dataset | ISO 19115 metadata form to document a new dataset |
| Lineage viewer | Step-by-step transformation history for any dataset |
| Statistics | Dataset counts by domain, classification, and format |

---

## ISO 19115 Metadata Fields

| Category | Fields |
|----------|--------|
| Identification | title, abstract, record_id, domain, classification |
| Spatial | geometry_type, CRS, bounding_box |
| Temporal | date_created, date_modified, temporal_extent, update_frequency |
| Provenance | source_organization, data_steward, source_url, lineage |
| Distribution | format, access_url, licence |

---

## Data Domains

| Domain | Scope | Classification |
|--------|-------|----------------|
| DD01 | Reference Geospatial Data | Public / Restricted |
| DD02 | Operational Field Data | Restricted / Confidential |
| DD03 | Health & Epidemiological Data | Confidential |
| DD04 | Logistics & Supply Chain | Restricted |
| DD05 | Context & Security Data | Confidential / Sensitive |

---

## Related Projects

| Project | Description |
|---------|-------------|
| [humanitarian-gis-governance](https://github.com/sanyamsin/humanitarian-gis-governance) | DAMA-DMBOK v2 governance framework |
| [geodata-quality-pipeline](https://github.com/sanyamsin/geodata-quality-pipeline) | Automated geospatial quality monitoring |

---

## Author

**Serge-Alain NYAMSIN** - GIS Data Governance & Humanitarian Data Engineering  
[github.com/sanyamsin](https://github.com/sanyamsin)

---

## License

MIT License