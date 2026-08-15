from pathlib import Path

from jd_helper import documents


def test_document():
    doc = documents.Document(Path(__file__))
    assert doc.title == "test_documents.py"


def test_find_documents():
    our_root_dir = Path(__file__).parent.parent
    # We have a readme and a changelog.
    docs = documents.find_documents(our_root_dir)
    assert len(docs) == 2
    assert docs[1].title == "README.md"
