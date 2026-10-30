import ast
import io
import os
import pathlib
import tokenize

import pytest

import cvlite
from cvlite.glossary import GLOSSARY

LABS = range(1, 9)
PACKAGE_DIR = pathlib.Path(cvlite.__file__).parent
DATASET = os.environ.get("CVLITE_DATASET")


def has_comments(source):
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    return any(token.type == tokenize.COMMENT for token in tokens)


def has_docstrings(source):
    tree = ast.parse(source)
    nodes = [tree] + [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    return any(ast.get_docstring(n) is not None for n in nodes)


@pytest.mark.parametrize("lab", LABS)
def test_code_compiles_without_comments_or_docstrings(lab):
    source = cvlite.get_code(lab, "/content/some file's name.jpg")
    compile(source, "lab", "exec")
    assert not has_comments(source)
    assert not has_docstrings(source)
    assert "__PATH__" not in source


UNSAFE_IN_COLAB = {"cv2.imshow", "cv2.waitKey", "cv2.destroyAllWindows", "cv2.destroyWindow", "cv2.namedWindow",
                   "cv2.selectROI", "cv2.selectROIs", "cv2.setMouseCallback", "cv2.createTrackbar", "cv2.grabCut"}


@pytest.mark.parametrize("lab", LABS)
def test_no_gui_or_unsafe_functions(lab):
    used = {key for key, _ in cvlite.functions_used(lab)}
    assert used & UNSAFE_IN_COLAB == set()


@pytest.mark.parametrize("lab", LABS)
def test_every_function_is_explained(lab):
    missing = [key for key, _ in cvlite.functions_used(lab) if key not in GLOSSARY]
    assert missing == []
    text = cvlite.get_explanation(lab)
    for key, _ in cvlite.functions_used(lab):
        assert GLOSSARY[key][0] in text


def test_no_unused_glossary_entries():
    used = {key for lab in LABS for key, _ in cvlite.functions_used(lab)}
    assert set(GLOSSARY) - used == set()


@pytest.mark.parametrize("path", sorted(PACKAGE_DIR.rglob("*.py")), ids=lambda p: p.name)
def test_package_source_has_no_comments_or_docstrings(path):
    source = path.read_text()
    assert not has_comments(source)
    assert not has_docstrings(source)


def test_version_matches_pyproject():
    pyproject = (PACKAGE_DIR.parent / "pyproject.toml").read_text()
    assert 'version = "' + cvlite.__version__ + '"' in pyproject


def test_path_is_inserted():
    assert "image_path = '/content/cat.png'" in cvlite.get_code(1, "/content/cat.png")
    assert "video_path = '/content/clip.mp4'" in cvlite.get_code(7, "/content/clip.mp4")


@pytest.mark.parametrize("bad", [0, 9, "x", None])
def test_bad_lab_number(bad):
    with pytest.raises(ValueError):
        cvlite.get_code(bad)


INPUTS = {
    1: "image/1.jpg", 2: "image/2.jpeg", 3: "image/3.jpg", 4: "image/1.jpg",
    5: "image/2.jpeg", 6: "image/2.jpeg", 7: "video/1.mp4", 8: "video/1.mp4",
}


@pytest.mark.skipif(DATASET is None, reason="set CVLITE_DATASET to the Dataset folder to run the labs")
@pytest.mark.parametrize("lab", LABS)
def test_lab_runs(lab, tmp_path, monkeypatch):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out_dir = pathlib.Path(os.environ.get("CVLITE_FIGURES", tmp_path))
    out_dir.mkdir(parents=True, exist_ok=True)
    shown = []

    def save_instead_of_show():
        shown.append(1)
        plt.savefig(out_dir / ("lab" + str(lab) + "_fig" + str(len(shown)) + ".png"), dpi=60)
        plt.close("all")

    monkeypatch.setattr(plt, "show", save_instead_of_show)
    monkeypatch.chdir(tmp_path)
    cvlite.run(lab, os.path.join(DATASET, INPUTS[lab]))
    assert shown
