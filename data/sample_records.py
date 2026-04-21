"""
data/sample_records.py
=======================
Generates sample metadata records for demo purposes.
Run this script once to populate the catalogue.

Usage:
    python data/sample_records.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from catalogue.metadata import MetadataRecord
from catalogue.catalogue import GeoCatalogue
from catalogue.lineage import LineageStore, create_sample_lineage


def generate_sample_records():
    """Creates realistic sample metadata records."""

    catalogue = GeoCatalogue()
    lineage_store = LineageStore()

    records = [
        MetadataRecord(
            title="Limites administratives RCA — Niveau 1",
            abstract="Limites administratives de la République Centrafricaine au niveau préfectoral (admin1). Source officielle OCHA COD. Utilisées pour la cartographie opérationnelle MSF et le ciblage des zones d'intervention.",
            domain="DD01",
            classification="Public",
            geometry_type="MultiPolygon",
            coordinate_reference_system="EPSG:4326",
            source_organization="OCHA HDX",
            data_steward="GIS Data Steward — Reference",
            update_frequency="quarterly",
            format="GeoPackage",
            keywords=["boundaries", "admin", "CAR", "RCA", "OCHA", "COD"],
            topic_category="boundaries",
            bounding_box={"west": 14.42, "east": 27.46, "south": 2.22, "north": 11.00},
            temporal_extent_start="2020-01-01",
            temporal_extent_end="present",
            source_url="https://data.humdata.org/dataset/cod-ab-caf",
            licence="CC BY 4.0",
            lineage_description="Téléchargé depuis HDX, converti en GeoPackage, reprojeté en EPSG:4326.",
            access_url="data/sample_records/rca_admin1.gpkg"
        ),

        MetadataRecord(
            title="Zones d'intervention — Programme RCA 2023-2025",
            abstract="Polygones des zones géographiques d'intervention du programme de développement rural en RCA financé par l'UE FED. Inclut les zones de couverture des activités agriculture, eau et sécurité alimentaire.",
            domain="DD02",
            classification="Restricted",
            geometry_type="Polygon",
            coordinate_reference_system="EPSG:4326",
            source_organization="IRAM / Programme RCA",
            data_steward="GIS Data Steward — Operations",
            update_frequency="monthly",
            format="GeoJSON",
            keywords=["intervention", "RCA", "programme", "UE", "FED", "IRAM"],
            topic_category="boundaries",
            bounding_box={"west": 15.0, "east": 22.0, "south": 3.5, "north": 8.0},
            temporal_extent_start="2023-01-01",
            temporal_extent_end="2025-12-31",
            source_url="internal",
            licence="Internal use only",
            lineage_description="Délimitation terrain par équipes IRAM, numérisé sous QGIS, validé par coordination.",
            known_issues="Certaines zones frontalières nécessitent mise à jour suite aux déplacements de population.",
            access_url="data/sample_records/rca_intervention_zones.geojson"
        ),

        MetadataRecord(
            title="Formations sanitaires — Mauritanie",
            abstract="Localisation des formations sanitaires en Mauritanie : hôpitaux, centres de santé, postes de santé. Données collectées via OpenStreetMap et validées par le Ministère de la Santé. Utilisées pour l'analyse de l'accès aux soins.",
            domain="DD03",
            classification="Public",
            geometry_type="Point",
            coordinate_reference_system="EPSG:4326",
            source_organization="OpenStreetMap / Ministère Santé Mauritanie",
            data_steward="GIS Data Steward — Health",
            update_frequency="monthly",
            format="GeoPackage",
            keywords=["santé", "health", "hôpital", "Mauritanie", "OSM", "formations sanitaires"],
            topic_category="health",
            bounding_box={"west": -17.0, "east": -4.8, "south": 14.7, "north": 27.3},
            temporal_extent_start="2024-01-01",
            temporal_extent_end="present",
            source_url="https://overpass-api.de",
            licence="ODbL",
            lineage_description="Extraction Overpass API, validation terrain ACF, enrichissement attributaire.",
            access_url="data/sample_records/mrt_health_facilities.gpkg"
        ),

        MetadataRecord(
            title="Corridors logistiques — Sahel Ouest",
            abstract="Réseau de routes praticables et corridors logistiques pour les opérations humanitaires en Mauritanie, Mali et Sénégal. Inclut les points de passage, postes de contrôle et contraintes saisonnières.",
            domain="DD04",
            classification="Restricted",
            geometry_type="LineString",
            coordinate_reference_system="EPSG:4326",
            source_organization="OCHA / LogCluster",
            data_steward="GIS Data Steward — Logistics",
            update_frequency="monthly",
            format="GeoJSON",
            keywords=["logistique", "routes", "corridors", "Sahel", "humanitaire"],
            topic_category="logistics",
            bounding_box={"west": -17.0, "east": 4.0, "south": 10.0, "north": 25.0},
            temporal_extent_start="2024-06-01",
            temporal_extent_end="present",
            source_url="https://logcluster.org",
            licence="CC BY 4.0",
            lineage_description="Compilation LogCluster, validation terrain, ajout contraintes saisonnières.",
            known_issues="Routes saison des pluies non encore mises à jour pour 2025.",
            access_url="data/sample_records/sahel_logistics.geojson"
        ),

        MetadataRecord(
            title="Événements de conflit — RCA 2024-2025",
            abstract="Localisation géoréférencée des événements de conflit armé en République Centrafricaine. Source ACLED. Données agrégées par mois pour protéger la confidentialité opérationnelle. Utilisées pour l'analyse contextuelle et la planification sécuritaire.",
            domain="DD05",
            classification="Confidential",
            geometry_type="Point",
            coordinate_reference_system="EPSG:4326",
            source_organization="ACLED",
            data_steward="GIS Data Steward — Security",
            update_frequency="weekly",
            format="GeoJSON",
            keywords=["conflit", "sécurité", "ACLED", "RCA", "violence"],
            topic_category="security",
            bounding_box={"west": 14.42, "east": 27.46, "south": 2.22, "north": 11.00},
            temporal_extent_start="2024-01-01",
            temporal_extent_end="present",
            source_url="https://acleddata.com",
            licence="ACLED Terms of Use",
            lineage_description="Export ACLED API, agrégation mensuelle, suppression données sensibles, validation sécurité.",
            known_issues="Sous-déclaration possible dans zones d'accès limité.",
            access_url="data/sample_records/rca_conflict_2024.geojson"
        ),
    ]

    print(f"\nAdding {len(records)} sample records to catalogue...\n")

    for record in records:
        result = catalogue.add_record(record)
        if result["success"]:
            print(f"  ✓ Added: {record.title[:60]} (ID: {result['record_id']})")
            lineage = create_sample_lineage(result["record_id"], record.title)
            lineage_store.save(lineage)
            print(f"    └─ Lineage documented: {len(lineage.events)} events")
        else:
            print(f"  ✗ Failed: {record.title} — {result['errors']}")

    stats = catalogue.stats()
    print(f"\nCatalogue stats:")
    print(f"  Total records : {stats['total']}")
    print(f"  By domain     : {stats['by_domain']}")
    print(f"  By format     : {stats['by_format']}")


if __name__ == "__main__":
    generate_sample_records()