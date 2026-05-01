import shutil
import os
from datetime import datetime


DB_SOURCE = "toilets.db"
BACKUP_DIR = "backups"


def backup_database():
    if not os.path.exists(DB_SOURCE):
        raise FileNotFoundError(f"Database file '{DB_SOURCE}' not found")

    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"toilets_backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    shutil.copy2(DB_SOURCE, backup_path)
    size_kb = os.path.getsize(backup_path) / 1024
    print(f"Backup saved: {backup_path} ({size_kb:.1f} KB)")

    _remove_old_backups(keep=5)


def _remove_old_backups(keep: int):
    files = sorted([
        f for f in os.listdir(BACKUP_DIR) if f.endswith(".db")
    ])
    to_delete = files[:-keep] if len(files) > keep else []
    for f in to_delete:
        os.remove(os.path.join(BACKUP_DIR, f))
        print(f"Removed old backup: {f}")


if __name__ == "__main__":
    backup_database()
