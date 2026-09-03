import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from train_model import is_better  # noqa: E402


def test_first_model_always_promoted():
    assert is_better(new_rmse=1.5, old_rmse=None) is True


def test_lower_rmse_wins():
    assert is_better(new_rmse=0.9, old_rmse=1.2) is True


def test_higher_rmse_does_not_win():
    assert is_better(new_rmse=1.3, old_rmse=1.2) is False


def test_equal_rmse_does_not_promote():
    # Ties don't promote - avoids needlessly re-uploading/replacing an
    # equally-good model on every run.
    assert is_better(new_rmse=1.2, old_rmse=1.2) is False
