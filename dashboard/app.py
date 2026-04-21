"""
dashboard/app.py
=================
Streamlit interface for the Humanitarian Geo-Catalogue.
Allows discovery, search, and documentation of geospatial datasets.

Run:
    streamlit run dashboard/app.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import json
from datetime import datetime

from catalogue.catalogue import GeoCatalogue
from catalogue.metadata import MetadataRecord, VALID_DOMAINS, VALID_CLASSIFICATIONS
from catalogue.lineage import LineageStore
import yaml

# ── PAGE CONFIG ───────────────────────────────────────────────

st.set_page_config(
    page_title="Humanitarian Geo-Catalogue",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── INIT ──────────────────────────────────────────────────────

@st.cache_resource
def get_catalogue():
    return GeoCatalogue()

@st.cache_resource
def get_lineage_store():
    return LineageStore()

catalogue = get_catalogue()
lineage_store = get_lineage_store()

# ── CLASSIFICATION COLORS ────────────────────────────────────

CLASS_COLORS = {
    "Public":       "#1a7a4a",
    "Restricted":   "#b45309",
    "Confidential": "#c0392b",
    "Sensitive":    "#6c0f0f",
}

DOMAIN_LABELS = {
    "DD01": "Reference Geospatial",
    "DD02": "Operational Field",
    "DD03": "Health & Epidemiology",
    "DD04": "Logistics & Supply",
    "DD05": "Context & Security",
}

# ── SIDEBAR ───────────────────────────────────────────────────

def render_sidebar():
    st.sidebar.title("🗂️ Geo-Catalogue")
    st.sidebar.caption("ISO 19115 | DAMA-DMBOK v2")
    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        ["🔍 Discover datasets", "➕ Add dataset", "📋 Lineage viewer", "📊 Statistics"],
        label_visibility="collapsed"
    )

    st.sidebar.divider()
    stats = catalogue.stats()
    st.sidebar.metric("Total datasets", stats.get("total", 0))

    return page


# ── DISCOVER PAGE ─────────────────────────────────────────────

def render_discover():
    st.title("🔍 Discover datasets")
    st.caption("Search and filter the humanitarian geospatial data catalogue")

    # Search filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        query = st.text_input("Search", placeholder="boundaries, health, RCA...")
    with col2:
        domain = st.selectbox("Domain", ["All"] + list(DOMAIN_LABELS.keys()),
                              format_func=lambda x: "All domains" if x == "All" else f"{x} — {DOMAIN_LABELS.get(x, x)}")
    with col3:
        classification = st.selectbox("Classification", ["All"] + VALID_CLASSIFICATIONS)
    with col4:
        geometry_type = st.selectbox("Geometry type", ["All", "Point", "LineString", "Polygon", "MultiPolygon", "Raster"])

    results = catalogue.search(
        query=query,
        domain="" if domain == "All" else domain,
        classification="" if classification == "All" else classification,
        geometry_type="" if geometry_type == "All" else geometry_type,
    )

    st.divider()
    st.markdown(f"**{len(results)} dataset(s) found**")

    if not results:
        st.info("No datasets match your search criteria.")
        return

    for r in results:
        color = CLASS_COLORS.get(r.get("classification", ""), "#666")
        domain_label = DOMAIN_LABELS.get(r.get("domain", ""), r.get("domain", ""))

        with st.expander(f"**{r['title']}** — {domain_label}"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Abstract**")
                st.write(r.get("abstract", ""))
                if r.get("keywords"):
                    st.markdown("**Keywords:** " + " · ".join(f"`{k}`" for k in r["keywords"]))
                if r.get("lineage_description"):
                    st.markdown(f"**Lineage:** {r['lineage_description']}")
                if r.get("known_issues"):
                    st.warning(f"⚠️ Known issues: {r['known_issues']}")

            with col2:
                st.markdown(f"""
                | Field | Value |
                |-------|-------|
                | **ID** | `{r['record_id']}` |
                | **Domain** | {r['domain']} |
                | **Classification** | {r['classification']} |
                | **Format** | {r.get('format', 'N/A')} |
                | **Geometry** | {r.get('geometry_type', 'N/A')} |
                | **CRS** | {r.get('crs', 'N/A')} |
                | **Source** | {r.get('source_organization', 'N/A')} |
                | **Steward** | {r.get('data_steward', 'N/A')} |
                | **Updated** | {r.get('update_frequency', 'N/A')} |
                | **Licence** | {r.get('licence', 'N/A')} |
                | **Modified** | {r.get('date_modified', 'N/A')} |
                """)

                if r.get("bounding_box"):
                    bb = r["bounding_box"]
                    st.markdown(f"**Bounding box:** W:{bb.get('west')} E:{bb.get('east')} S:{bb.get('south')} N:{bb.get('north')}")


# ── ADD DATASET PAGE ──────────────────────────────────────────

def render_add():
    st.title("➕ Add dataset")
    st.caption("Document a new geospatial dataset — ISO 19115 metadata form")

    with st.form("add_record_form"):
        st.subheader("Mandatory fields")
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Title *", placeholder="Limites administratives RCA — Niveau 1")
            domain = st.selectbox("Domain *", VALID_DOMAINS,
                                  format_func=lambda x: f"{x} — {DOMAIN_LABELS.get(x, x)}")
            geometry_type = st.selectbox("Geometry type *",
                                         ["Point", "LineString", "Polygon", "MultiPolygon", "Raster", "Mixed"])
            source_organization = st.text_input("Source organization *", placeholder="OCHA HDX")
            update_frequency = st.selectbox("Update frequency *",
                                            ["daily", "weekly", "monthly", "quarterly", "annual", "irregular"])

        with col2:
            classification = st.selectbox("Classification *", VALID_CLASSIFICATIONS)
            crs = st.text_input("CRS *", value="EPSG:4326")
            fmt = st.selectbox("Format *",
                               ["GeoPackage", "GeoJSON", "Shapefile", "GeoTIFF", "PostGIS table", "WMS", "WFS", "CSV"])
            data_steward = st.text_input("Data steward *", placeholder="GIS Data Steward — Reference")
            topic_category = st.selectbox("Topic category",
                                          ["boundaries", "health", "logistics", "security",
                                           "population", "environment", "infrastructure", "water"])

        abstract = st.text_area("Abstract *", height=100,
                                placeholder="Description du dataset, son contenu, son usage opérationnel...")

        st.subheader("Optional fields")
        col3, col4 = st.columns(2)
        with col3:
            keywords = st.text_input("Keywords (comma-separated)", placeholder="boundaries, admin, RCA")
            source_url = st.text_input("Source URL", placeholder="https://data.humdata.org/...")
            licence = st.text_input("Licence", placeholder="CC BY 4.0")
            temporal_start = st.text_input("Temporal extent start", placeholder="2024-01-01")
        with col4:
            lineage = st.text_input("Lineage description", placeholder="Téléchargé depuis HDX, converti...")
            access_url = st.text_input("Access URL / path", placeholder="data/...")
            known_issues = st.text_input("Known issues", placeholder="...")
            temporal_end = st.text_input("Temporal extent end", placeholder="present")

        submitted = st.form_submit_button("Save to catalogue", use_container_width=True)

        if submitted:
            record = MetadataRecord(
                title=title,
                abstract=abstract,
                domain=domain,
                classification=classification,
                geometry_type=geometry_type,
                coordinate_reference_system=crs,
                source_organization=source_organization,
                data_steward=data_steward,
                update_frequency=update_frequency,
                format=fmt,
                keywords=[k.strip() for k in keywords.split(",") if k.strip()],
                topic_category=topic_category,
                source_url=source_url,
                licence=licence,
                lineage_description=lineage,
                access_url=access_url,
                known_issues=known_issues,
                temporal_extent_start=temporal_start,
                temporal_extent_end=temporal_end,
            )
            result = catalogue.add_record(record)
            if result["success"]:
                st.success(f"Dataset added successfully. ID: `{result['record_id']}`")
                st.cache_resource.clear()
            else:
                for error in result["errors"]:
                    st.error(error)


# ── LINEAGE VIEWER ────────────────────────────────────────────

def render_lineage():
    st.title("📋 Lineage viewer")
    st.caption("Trace the origin and transformation history of datasets")

    records = catalogue.list_records()
    if not records:
        st.info("No records in catalogue. Add datasets first.")
        return

    record_options = {r["record_id"]: r["title"] for r in records}
    selected_id = st.selectbox(
        "Select dataset",
        list(record_options.keys()),
        format_func=lambda x: f"{x} — {record_options[x][:60]}"
    )

    if selected_id:
        lineage_data = lineage_store.load(selected_id)
        if not lineage_data:
            st.info("No lineage documented for this dataset.")
            return

        st.markdown(f"**Dataset:** {lineage_data['dataset_title']}")
        st.markdown(f"**Events:** {len(lineage_data['events'])}")
        st.divider()

        EVENT_ICONS = {
            "acquisition": "⬇️",
            "transformation": "⚙️",
            "validation": "✅",
            "publication": "📢",
        }

        for i, event in enumerate(lineage_data["events"]):
            icon = EVENT_ICONS.get(event["event_type"], "•")
            with st.expander(f"{icon} {i+1}. {event['event_type'].upper()} — {event['description'][:60]}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Type:** {event['event_type']}")
                    st.markdown(f"**Description:** {event['description']}")
                    st.markdown(f"**Performed by:** {event['performed_by']}")
                with col2:
                    st.markdown(f"**Tool used:** {event.get('tool_used', 'N/A')}")
                    st.markdown(f"**Timestamp:** {event.get('timestamp', 'N/A')[:19]}")
                    if event.get("notes"):
                        st.markdown(f"**Notes:** {event['notes']}")


# ── STATISTICS PAGE ───────────────────────────────────────────

def render_statistics():
    st.title("📊 Catalogue statistics")

    stats = catalogue.stats()
    records = catalogue.list_records()

    if not records:
        st.info("No records in catalogue.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total datasets", stats["total"])
    col2.metric("Domains covered", len(stats.get("by_domain", {})))
    col3.metric("Formats", len(stats.get("by_format", {})))

    st.divider()

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("**By domain**")
        domain_data = stats.get("by_domain", {})
        for d, count in domain_data.items():
            label = DOMAIN_LABELS.get(d, d)
            st.markdown(f"- **{d}** {label}: {count}")

    with col5:
        st.markdown("**By classification**")
        class_data = stats.get("by_classification", {})
        for c, count in class_data.items():
            color = CLASS_COLORS.get(c, "#666")
            st.markdown(f"- **{c}**: {count}")

    st.divider()
    st.markdown("**All records**")
    df = pd.DataFrame([{
        "ID": r["record_id"],
        "Title": r["title"][:50],
        "Domain": r["domain"],
        "Classification": r["classification"],
        "Format": r.get("format", ""),
        "Steward": r.get("data_steward", ""),
        "Modified": r.get("date_modified", ""),
    } for r in records])
    st.dataframe(df, hide_index=True, use_container_width=True)


# ── MAIN ──────────────────────────────────────────────────────

def main():
    page = render_sidebar()

    if page == "🔍 Discover datasets":
        render_discover()
    elif page == "➕ Add dataset":
        render_add()
    elif page == "📋 Lineage viewer":
        render_lineage()
    elif page == "📊 Statistics":
        render_statistics()

    st.divider()
    st.caption(
        f"github.com/sanyamsin/humanitarian-geo-catalogue  |  "
        f"ISO 19115:2014  |  DAMA-DMBOK v2  |  "
        f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC"
    )


if __name__ == "__main__":
    main()