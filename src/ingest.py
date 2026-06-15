from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Document:
    title: str
    content: str
    path: str
    url: str | None = None


HEADING_PATTERN = re.compile(r"^##\s+(.+)$", re.MULTILINE)
URL_PATTERN = re.compile(r"https?://[^\s)]+")


def split_markdown(text: str, path: str) -> list[Document]:
    """Split Markdown on level-two headings into self-contained documents."""
    matches = list(HEADING_PATTERN.finditer(text))
    if not matches:
        title = Path(path).stem.replace("_", " ").title()
        return [Document(title=title, content=text.strip(), path=path)]

    documents = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        content = text[match.end() : end].strip()
        urls = URL_PATTERN.findall(content)
        documents.append(
            Document(
                title=match.group(1).strip(),
                content=content,
                path=path,
                url=urls[0] if urls else None,
            )
        )
    return documents


def load_knowledge(directory: str | Path) -> list[Document]:
    knowledge_dir = Path(directory)
    documents = []
    for markdown_file in sorted(knowledge_dir.glob("*.md")):
        documents.extend(
            split_markdown(
                markdown_file.read_text(encoding="utf-8"),
                markdown_file.as_posix(),
            )
        )
    return documents
