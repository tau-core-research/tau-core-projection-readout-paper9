import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper9_submission_source"


def test_publication_files_exist():
    required = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "CITATION.cff",
        ROOT / "DATA_NOTICE.md",
        ROOT / "requirements.txt",
        SOURCE / "main.tex",
        SOURCE / "refs.bib",
        SOURCE / "main.pdf",
        SOURCE / "figures",
        ROOT / "scripts" / "build_arxiv_source.py",
        ROOT / "scripts" / "reproduce.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert not missing


def test_claim_boundary_markers_present():
    tex = (SOURCE / "main.tex").read_text()
    assert "source-frozen candidate audit" in tex
    assert "not evidence on UGC12506" in tex
    assert "post-diagnostic transfer candidate" in tex
    assert "population-level gravitational law is validated here" in tex


def test_arxiv_zip_is_source_only():
    archive = ROOT / "arxiv_submission_source.zip"
    assert archive.exists()
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
    assert all(not name.endswith(".aux") for name in names)
