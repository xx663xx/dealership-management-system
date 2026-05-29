import base64
import csv
import hashlib
import os
import shutil
import tomllib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
DIST_DIR = ROOT / "dist"
PACKAGE_DIR = ROOT / "packages" / "dealership_core"


def normalized_distribution_name(name):
    return name.replace("-", "_")


def wheel_hash(data):
    digest = hashlib.sha256(data).digest()
    encoded = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return f"sha256={encoded}"


def read_project_metadata():
    with open(PYPROJECT, "rb") as file:
        project = tomllib.load(file)["project"]
    return {
        "name": project["name"],
        "version": project["version"],
        "description": project.get("description", ""),
        "requires_python": project.get("requires-python", ""),
    }


def add_file(wheel, records, source_path, wheel_path):
    data = source_path.read_bytes()
    wheel.writestr(wheel_path, data)
    records.append((wheel_path, wheel_hash(data), str(len(data))))


def add_text(wheel, records, wheel_path, text):
    data = text.encode("utf-8")
    wheel.writestr(wheel_path, data)
    records.append((wheel_path, wheel_hash(data), str(len(data))))


def build_wheel():
    metadata = read_project_metadata()
    distribution = normalized_distribution_name(metadata["name"])
    version = metadata["version"]
    dist_info = f"{distribution}-{version}.dist-info"
    wheel_name = f"{distribution}-{version}-py3-none-any.whl"

    shutil.rmtree(DIST_DIR, ignore_errors=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    wheel_path = DIST_DIR / wheel_name
    records = []

    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as wheel:
        package_root = ROOT / "packages"
        for source_path in sorted(PACKAGE_DIR.rglob("*.py")):
            wheel_file_path = source_path.relative_to(ROOT).as_posix()
            add_file(wheel, records, source_path, wheel_file_path)

        package_init = package_root / "__init__.py"
        add_file(wheel, records, package_init, package_init.relative_to(ROOT).as_posix())

        metadata_text = "\n".join(
            [
                "Metadata-Version: 2.1",
                f"Name: {metadata['name']}",
                f"Version: {version}",
                f"Summary: {metadata['description']}",
                f"Requires-Python: {metadata['requires_python']}",
                "",
            ]
        )
        add_text(wheel, records, f"{dist_info}/METADATA", metadata_text)

        wheel_text = "\n".join(
            [
                "Wheel-Version: 1.0",
                "Generator: scripts/build_core_wheel.py",
                "Root-Is-Purelib: true",
                "Tag: py3-none-any",
                "",
            ]
        )
        add_text(wheel, records, f"{dist_info}/WHEEL", wheel_text)

        top_level_text = "packages\n"
        add_text(wheel, records, f"{dist_info}/top_level.txt", top_level_text)

        record_path = f"{dist_info}/RECORD"
        records.append((record_path, "", ""))
        record_lines = []
        for row in records:
            output = []
            csv.writer(output := _CsvLine()).writerow(row)
            record_lines.append(str(output))
        wheel.writestr(record_path, "".join(record_lines).encode("utf-8"))

    print(f"Built {os.path.relpath(wheel_path, ROOT)}")


class _CsvLine(list):
    def write(self, value):
        self.append(value)

    def __str__(self):
        return "".join(self)


if __name__ == "__main__":
    build_wheel()
