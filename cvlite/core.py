import ast
import builtins
import importlib
import textwrap

from .glossary import GLOSSARY

LAB_NUMBERS = list(range(1, 9))
WIDTH = 100


def _lab(number):
    try:
        number = int(number)
    except (TypeError, ValueError):
        raise ValueError("Lab number must be an integer from 1 to 8, got " + repr(number)) from None
    if number not in LAB_NUMBERS:
        raise ValueError("Lab number must be from 1 to 8, got " + str(number))
    return importlib.import_module(".labs.lab" + str(number), __package__)


def get_code(lab, path=None):
    module = _lab(lab)
    if path is None:
        path = module.DEFAULT_PATH
    return module.CODE.replace("__PATH__", repr(str(path)))


def code(lab, path=None):
    print(get_code(lab, path))


def run(lab, path=None):
    source = get_code(lab, path)
    exec(compile(source, "<cvlite lab " + str(lab) + ">", "exec"), {"__name__": "__main__"})


def _dotted(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts)), node.id
    return None, None


def _key(node, imported):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        name, root = _dotted(node)
        if name is not None and (root in imported or hasattr(builtins, root)):
            return name
        return "." + node.attr
    return None


def functions_used(lab):
    source = _lab(lab).CODE.replace("__PATH__", "''")
    tree = ast.parse(source)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update((a.asname or a.name).split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.update(a.asname or a.name for a in node.names)
    found = {}
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Call):
            targets.append(node.func)
            targets.extend(k.value for k in node.keywords if k.arg == "key")
        for target in targets:
            key = _key(target, imported)
            if key is None:
                continue
            snippet = ast.get_source_segment(source, node if target is node.func else target)
            position = (target.lineno, target.col_offset)
            if key not in found or position < found[key][0]:
                found[key] = (position, snippet)
    ordered = sorted(found.items(), key=lambda item: item[1][0])
    return [(key, snippet) for key, (position, snippet) in ordered]


def _wrap(text, indent):
    return textwrap.fill(text, WIDTH, initial_indent=indent, subsequent_indent=indent)


def get_explanation(lab):
    module = _lab(lab)
    number = int(lab)
    lines = ["=" * WIDTH, "LAB " + str(number) + ": " + module.TITLE.upper(), "Input: " + module.INPUT, "=" * WIDTH, ""]
    lines += ["AIM", _wrap(module.AIM, "  "), ""]
    lines.append("WHAT THE PROGRAM DOES (STEP BY STEP)")
    for i, step in enumerate(module.STEPS, 1):
        lines.append(textwrap.fill(step, WIDTH, initial_indent="  " + str(i) + ". ", subsequent_indent="     "))
    lines += ["", "KEY THEORY"]
    for point in module.THEORY:
        lines.append(textwrap.fill(point, WIDTH, initial_indent="  - ", subsequent_indent="    "))
    lines += ["", "EVERY FUNCTION USED (in the order it appears in the code)", "-" * WIDTH]
    for key, snippet in functions_used(number):
        title, library, text = GLOSSARY[key]
        lines.append(title + "   [" + library + "]")
        lines.append(_wrap("Used as: " + " ".join(snippet.split()), "    "))
        lines.append(_wrap(text, "    "))
        lines.append("")
    return "\n".join(lines)


def explain(lab):
    print(get_explanation(lab))


def get_labs():
    rows = []
    for number in LAB_NUMBERS:
        module = _lab(number)
        rows.append((number, module.TITLE, module.INPUT))
    return rows


def labs():
    print("Lab  Input            Title")
    print("---  ---------------  " + "-" * 60)
    for number, title, kind in get_labs():
        print(str(number).rjust(3) + "  " + kind.ljust(15) + "  " + title)


def usage():
    print("\n".join([
        "cvlite",
        "",
        "  import cvlite",
        "  cvlite.labs()                              list all labs",
        "  cvlite.code(3, '/content/photo.jpg')       print ready-to-run code for lab 3 using that image",
        "  cvlite.explain(3)                          explain the lab and every function it uses",
        "  cvlite.run(3, '/content/photo.jpg')        run lab 3 directly on that image",
        "  cvlite.get_code(3, '/content/photo.jpg')   return the code as a string",
        "",
        "Labs 1-6 take an image path, lab 7 takes a video path, lab 8 takes a video or an image path.",
    ]))
