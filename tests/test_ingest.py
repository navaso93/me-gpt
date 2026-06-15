from src.ingest import split_markdown


def test_split_markdown_creates_sections_with_links():
    documents = split_markdown(
        "# Projects\n\n## Example\nUseful detail.\nRepo: https://example.com/repo",
        "knowledge/projects.md",
    )

    assert len(documents) == 1
    assert documents[0].title == "Example"
    assert documents[0].url == "https://example.com/repo"
