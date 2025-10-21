import os
import json
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "mitre_attack")

# MongoDB collections for each domain
COLLECTIONS = {
    "enterprise": "enterprise_attack",
    "mobile": "mobile_attack",
    "ics": "ics_attack"
}

# MITRE ATT&CK JSON URLs
MITRE_URLS = {
    "enterprise": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json",
    "mobile": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json",
    "ics": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json"
}

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Transform STIX object
def transform_stix_object(obj):
    if obj.get("type") != "attack-pattern":
        return None
    kill_phases = [p.get("phase_name") for p in obj.get("kill_chain_phases", [])]
    ext_refs = [{"source_name": r.get("source_name"), "url": r.get("url")} for r in obj.get("external_references", [])]
    return {
        "id": obj.get("id"),
        "name": obj.get("name"),
        "description": obj.get("description"),
        "created": obj.get("created"),
        "modified": obj.get("modified"),
        "kill_chain_phases": kill_phases,
        "external_references": ext_refs
    }

# ETL for a single domain
def run_etl(domain_name):
    print(f"\n=== Processing {domain_name.upper()} ATT&CK ===")
    url = MITRE_URLS[domain_name]
    collection_name = COLLECTIONS[domain_name]

    # Extract
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Failed to fetch {domain_name} data. Status code: {resp.status_code}")
        return
    objects = resp.json().get("objects", [])
    print(f"Total STIX objects fetched: {len(objects)}")

    # Transform
    transformed_records = [transform_stix_object(o) for o in objects if transform_stix_object(o)]
    print(f"Total attack-patterns transformed: {len(transformed_records)}")

    # Load
    collection = db[collection_name]
    collection.drop()  # clear existing data
    if transformed_records:
        collection.insert_many(transformed_records)
        print(f"Inserted {len(transformed_records)} records into MongoDB collection: {collection_name}")

# Main ETL loop
if __name__ == "__main__":
    for domain in ["enterprise", "mobile", "ics"]:
        run_etl(domain)
    print("\n✅ ETL process completed for all ATT&CK domains.")
