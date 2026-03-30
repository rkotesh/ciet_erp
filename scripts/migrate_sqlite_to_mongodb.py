import argparse
import base64
import datetime as dt
import decimal
import json
import os
import sqlite3
from pathlib import Path

from pymongo import MongoClient


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SQLITE_PATH = PROJECT_ROOT / "db.sqlite3"


def normalize_value(value):
    if isinstance(value, bytes):
        return {
            "_type": "bytes",
            "base64": base64.b64encode(value).decode("ascii"),
        }
    if isinstance(value, (dt.date, dt.datetime, dt.time)):
        return value.isoformat()
    if isinstance(value, decimal.Decimal):
        return str(value)
    return value


def get_table_names(connection):
    cursor = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    return [row[0] for row in cursor.fetchall()]


def get_primary_key_columns(connection, table_name):
    cursor = connection.execute(f'PRAGMA table_info("{table_name}")')
    rows = cursor.fetchall()
    primary_keys = [row[1] for row in rows if row[5] > 0]
    return primary_keys


def build_documents(connection, table_name):
    cursor = connection.execute(f'SELECT * FROM "{table_name}"')
    columns = [description[0] for description in cursor.description]
    documents = []
    for row in cursor.fetchall():
        document = {}
        for column, value in zip(columns, row):
            document[column] = normalize_value(value)
        documents.append(document)
    return documents


def build_upsert_filter(document, primary_keys):
    if primary_keys:
        return {key: document.get(key) for key in primary_keys}
    return document


def migrate(sqlite_path, mongodb_uri, mongodb_name, drop_existing):
    sqlite_connection = sqlite3.connect(sqlite_path)
    sqlite_connection.row_factory = sqlite3.Row

    mongo_client = MongoClient(mongodb_uri)
    mongo_db = mongo_client[mongodb_name]

    summary = []
    for table_name in get_table_names(sqlite_connection):
        documents = build_documents(sqlite_connection, table_name)
        collection = mongo_db[table_name]
        primary_keys = get_primary_key_columns(sqlite_connection, table_name)

        if drop_existing:
            collection.drop()

        migrated = 0
        for document in documents:
            filter_query = build_upsert_filter(document, primary_keys)
            collection.replace_one(filter_query, document, upsert=True)
            migrated += 1

        summary.append(
            {
                "table": table_name,
                "rows": len(documents),
                "primary_keys": primary_keys,
                "migrated": migrated,
            }
        )

    sqlite_connection.close()
    mongo_client.close()
    return summary


def parse_args():
    parser = argparse.ArgumentParser(description="Copy SQLite tables into MongoDB collections.")
    parser.add_argument(
        "--sqlite-path",
        default=str(DEFAULT_SQLITE_PATH),
        help="Path to the SQLite database file.",
    )
    parser.add_argument(
        "--mongodb-uri",
        default=os.environ.get("MONGODB_URI", ""),
        help="MongoDB connection URI.",
    )
    parser.add_argument(
        "--mongodb-name",
        default=os.environ.get("MONGODB_NAME", "erp_portal"),
        help="MongoDB database name.",
    )
    parser.add_argument(
        "--drop-existing",
        action="store_true",
        help="Drop collections before inserting migrated data.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.mongodb_uri:
        raise SystemExit("Missing MongoDB URI. Set MONGODB_URI or pass --mongodb-uri.")

    summary = migrate(
        sqlite_path=args.sqlite_path,
        mongodb_uri=args.mongodb_uri,
        mongodb_name=args.mongodb_name,
        drop_existing=args.drop_existing,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
