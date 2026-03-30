import datetime as dt
import os
import sys
from pathlib import Path
from decimal import Decimal, InvalidOperation

import django
from bson import Decimal128
from pymongo import MongoClient
from django.conf import settings
from django.db import models
from django.db.migrations.recorder import MigrationRecorder
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime, parse_time


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()


def normalize_datetime(value):
    if value is None or isinstance(value, dt.datetime):
        return value
    if not isinstance(value, str):
        return value
    parsed = parse_datetime(value)
    if parsed is None:
        return value
    if timezone.is_aware(parsed):
        parsed = timezone.make_naive(parsed, timezone.get_current_timezone())
    return parsed


def normalize_date(value):
    if value is None or isinstance(value, dt.datetime):
        return value
    if not isinstance(value, str):
        return value
    parsed = parse_date(value)
    if parsed is None:
        return value
    return dt.datetime.combine(parsed, dt.time.min)


def normalize_time(value):
    if value is None or isinstance(value, dt.datetime):
        return value
    if not isinstance(value, str):
        return value
    parsed = parse_time(value)
    if parsed is None:
        return value
    return dt.datetime.combine(dt.date.min, parsed)


def normalize_decimal(value):
    if value is None or isinstance(value, Decimal128):
        return value
    if isinstance(value, (int, float, Decimal)):
        return Decimal128(str(value))
    if not isinstance(value, str):
        return value
    try:
        return Decimal128(str(Decimal(value)))
    except (InvalidOperation, ValueError):
        return value


def normalize_boolean(value):
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    return value


def get_model_field_map():
    table_field_map = {}
    for model in django.apps.apps.get_models(include_auto_created=True):
        fields = {}
        for field in model._meta.local_fields:
            fields[field.column] = field
        table_field_map[model._meta.db_table] = fields

    migration_model = MigrationRecorder.Migration
    table_field_map[migration_model._meta.db_table] = {
        field.column: field for field in migration_model._meta.local_fields
    }
    return table_field_map


def convert_value(field, value):
    if isinstance(field, models.DateTimeField):
        return normalize_datetime(value)
    if isinstance(field, models.DateField):
        return normalize_date(value)
    if isinstance(field, models.TimeField):
        return normalize_time(value)
    if isinstance(field, models.DecimalField):
        return normalize_decimal(value)
    if isinstance(field, models.BooleanField):
        return normalize_boolean(value)
    return value


def repair():
    client = MongoClient(settings.DATABASES["default"]["HOST"])
    db = client[settings.DATABASES["default"]["NAME"]]
    table_field_map = get_model_field_map()
    summary = []

    for table_name, field_map in table_field_map.items():
        collection = db[table_name]
        updated_docs = 0

        for document in collection.find({}):
            updates = {}
            for column, field in field_map.items():
                if column not in document:
                    continue
                converted = convert_value(field, document[column])
                if converted != document[column]:
                    updates[column] = converted

            if updates:
                collection.update_one({"_id": document["_id"]}, {"$set": updates})
                updated_docs += 1

        if updated_docs:
            summary.append((table_name, updated_docs))

    client.close()
    return summary


if __name__ == "__main__":
    result = repair()
    for table_name, updated_docs in result:
        print(f"{table_name}: updated {updated_docs} documents")
