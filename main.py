import os
import shutil
import tempfile
from pathlib import Path


def delete_files_in(folder):
    total_deleted = 0
    folder = Path(folder)

    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        return total_deleted

    for item in folder.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                size = item.stat().st_size
                os.remove(item)
                total_deleted += size
            elif item.is_dir():
                size = get_folder_size(item)
                shutil.rmtree(item)
                total_deleted += size
        except Exception as e:
            print(f"⚠️ Could not delete {item}: {e}")

    return total_deleted


def get_folder_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total += os.path.getsize(fp)
            except:
                pass
    return total


def human_readable_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


# Paths to clean
paths = [
    tempfile.gettempdir(),  # %temp%
    r"C:\Windows\Temp",  # system temp
    r"C:\Windows\Prefetch",  # prefetch
]

print("🧹 Cleaning temporary folders...")

total_freed = 0
for path in paths:
    print(f"➡️ Cleaning: {path}")
    freed = delete_files_in(path)
    print(f"✅ Freed {human_readable_size(freed)} from {path}\n")
    total_freed += freed

print(f"\n🎉 Total Space Freed: {human_readable_size(total_freed)}")
