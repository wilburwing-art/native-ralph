"""File system tools for reading and writing project files."""

from pathlib import Path

from adk_agents.config import get_project_root


def _resolve_path(file_path: str) -> Path:
    """Resolve a file path relative to the project root if not absolute."""
    p = Path(file_path)
    if p.is_absolute():
        return p
    return get_project_root() / p


def read_file(file_path: str) -> dict:
    """Read the contents of a file.

    Args:
        file_path: Path to the file (absolute or relative to project root).

    Returns:
        dict with status and file content or error message.
    """
    path = _resolve_path(file_path)
    if not path.exists():
        return {"status": "error", "error": f"File not found: {path}"}
    if not path.is_file():
        return {"status": "error", "error": f"Not a file: {path}"}

    try:
        content = path.read_text(encoding="utf-8")
        return {"status": "ok", "path": str(path), "content": content}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def write_file(file_path: str, content: str) -> dict:
    """Write content to a file, creating parent directories as needed.

    Args:
        file_path: Path to the file (absolute or relative to project root).
        content: Text content to write.

    Returns:
        dict with status and the written file path or error message.
    """
    path = _resolve_path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return {"status": "ok", "path": str(path)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def list_files(directory: str = ".", pattern: str = "*") -> dict:
    """List files in a directory matching a glob pattern.

    Args:
        directory: Directory to list (absolute or relative to project root).
        pattern: Glob pattern to match (default: all files).

    Returns:
        dict with status and list of matching file paths.
    """
    path = _resolve_path(directory)
    if not path.exists():
        return {"status": "error", "error": f"Directory not found: {path}"}
    if not path.is_dir():
        return {"status": "error", "error": f"Not a directory: {path}"}

    try:
        files = sorted(str(f.relative_to(path)) for f in path.glob(pattern) if f.is_file())
        return {"status": "ok", "directory": str(path), "files": files}
    except Exception as e:
        return {"status": "error", "error": str(e)}
