
from pathlib import Path


def test_project_required_files_exist():
    project_root = Path(__file__).resolve().parent.parent

    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "data/customers.csv",
        "data/products.csv",
    ]

    for file_name in required_files:
        assert (project_root / file_name).is_file(), (
            f"Required project file is missing: {file_name}"
        )


def test_output_directory_exists():
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "output"

    assert output_dir.is_dir()
