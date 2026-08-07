from pathlib import Path

from jd_helper import utils


def test_area_pattern(tmp_path: Path):
    dir1 = tmp_path / "40_correct-name"
    dir2 = tmp_path / "50-wrong-dash-instead-of-underscore"
    dir3 = tmp_path / "62_wrong-not-a-multiple-of-ten"
    dir4 = tmp_path / "70.34_wrong-is-an-ID"
    dir1.mkdir()
    dir2.mkdir()
    dir3.mkdir()
    dir4.mkdir()
    assert len(list(tmp_path.glob(utils.AREA_PATTERN))) == 1


def test_category_pattern(tmp_path: Path):
    dir1 = tmp_path / "40_correct-name-zero-allowed"
    dir2 = tmp_path / "50-wrong-dash-instead-of-underscore"
    dir3 = tmp_path / "62_also-correct-name"
    dir4 = tmp_path / "70.34_wrong-is-an-ID"
    dir1.mkdir()
    dir2.mkdir()
    dir3.mkdir()
    dir4.mkdir()
    assert len(list(tmp_path.glob(utils.CATEGORY_PATTERN))) == 2


def test_id_pattern(tmp_path: Path):
    dir1 = tmp_path / "40_wrong-is-area"
    dir2 = tmp_path / "51.23-wrong-dash-instead-of-underscore"
    dir3 = tmp_path / "62_wrong-is-category"
    dir4 = tmp_path / "72.34_correct"
    dir1.mkdir()
    dir2.mkdir()
    dir3.mkdir()
    dir4.mkdir()
    assert len(list(tmp_path.glob(utils.ID_PATTERN))) == 1
