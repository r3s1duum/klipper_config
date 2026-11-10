"""Check or format the text files of the Klipper config repo.

Rules:
    * no trailing whitespace
    * no CRLF line endings (LF only)
    * no tabs in leading whitespace
    * leading whitespace is a multiple of the indent width
    (2 spaces, 4 for .py files), never less than one indent
    * file ends with exactly one newline

Inside multi-line gcode/Jinja bodies only whitespace changes, which Klipper
and Jinja ignore there.
"""
import os
import subprocess
import sys

DEFAULT_INDENT = 2
INDENT_BY_SUFFIX = {".py": 4}


def indent_for(path):
    return INDENT_BY_SUFFIX.get(os.path.splitext(path)[1], DEFAULT_INDENT)


def format_text(text, indent):
    """Return (fixed_text, list_of_problem_descriptions)."""
    problems = []
    if "\r" in text:
        problems.append("CRLF or CR line endings")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    out = []
    for lineno, line in enumerate(text.split("\n"), 1):
        stripped = line.rstrip(" \t")
        if stripped != line:
            problems.append(f"line {lineno}: trailing whitespace")
        body = stripped.lstrip(" \t")
        if body:
            leading = stripped[: len(stripped) - len(body)]
            if "\t" in leading:
                problems.append(f"line {lineno}: tab used for indentation")
            width = len(leading.expandtabs(indent))
            if width:
                fixed = max(indent, width - width % indent)
                if fixed != width:
                    problems.append(
                        f"line {lineno}: indent of {width} spaces, expected {fixed}"
                    )
                stripped = " " * fixed + body
        out.append(stripped)

    joined = "\n".join(out)
    result = joined.rstrip("\n") + "\n"
    if result != joined and joined.strip():
        problems.append("file must end with exactly one newline")
    return result, problems


def repo_root():
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def tracked_files(root):
    out = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
    ).stdout
    return [os.path.join(root, p) for p in out.splitlines()]


def main(args):
    """Run the tool. Returns the process exit code."""
    check_only = "--check" in args
    paths = [a for a in args if a != "--check"]
    root = repo_root()
    paths = [os.path.abspath(p) for p in paths] or tracked_files(root)

    failed = False
    for path in paths:
        try:
            with open(path, encoding="utf-8", newline="") as fh:
                original = fh.read()
        except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
            continue
        fixed, problems = format_text(original, indent_for(path))
        if not problems:
            continue
        name = os.path.relpath(path, root)
        if check_only:
            failed = True
            for problem in problems:
                print(f"{name}: {problem}")
        else:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(fixed)
            print(f"formatted {name} ({len(problems)} fix(es))")
    if not check_only:
        print("done")
    return 1 if failed else 0


def main_cli():
    sys.exit(main(sys.argv[1:]))
