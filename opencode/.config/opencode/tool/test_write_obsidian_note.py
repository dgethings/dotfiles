# /// script
# dependencies = [
#   "typer >= 0.20",
#   "pyyaml >= 6.0.0",
#   "pytest >= 9.0.0",
# ]
# ///
import pytest
from datetime import date
from unittest.mock import patch
import yaml

from write_obsidian_note import parse_frontmatter, main, Exit


class TestParseFrontmatter:
    def test_parse_frontmatter_simple(self):
        result = parse_frontmatter("key1:value1,key2:value2")
        parsed = yaml.safe_load(result)
        assert parsed == {"key1": "value1", "key2": "value2"}

    def test_parse_frontmatter_empty_string(self):
        result = parse_frontmatter("")
        parsed = yaml.safe_load(result)
        assert parsed == {}

    def test_parse_frontmatter_single_pair(self):
        result = parse_frontmatter("author:John")
        parsed = yaml.safe_load(result)
        assert parsed == {"author": "John"}


class TestWriteObsidianNote:
    @pytest.fixture
    def temp_vault(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()
        return vault

    def test_write_new_file(self, temp_vault):
        main(
            video_id="abc123",
            filename="test_note",
            tags="python,testing",
            contents="This is test content",
            vault_dir=temp_vault,
        )

        file_path = temp_vault / "test_note.md"
        assert file_path.exists()
        content = file_path.read_text()

        assert "This is test content" in content
        assert "python" in content
        assert "testing" in content

    def test_write_file_with_default_tags(self, temp_vault):
        main(
            video_id="xyz789",
            filename="default_tags",
            tags="custom",
            contents="Content with default tags",
            vault_dir=temp_vault,
        )

        file_path = temp_vault / "default_tags.md"
        content = file_path.read_text()

        parsed = yaml.safe_load(content)
        assert "youtube" in parsed["tags"]
        assert "video" in parsed["tags"]
        assert "custom" in parsed["tags"]

    def test_overwrite_prevents_existing_file_update(self, temp_vault):
        main(
            video_id="abc123",
            filename="note1",
            tags="tag1",
            contents="Original content",
            vault_dir=temp_vault,
        )

        original_content = (temp_vault / "note1.md").read_text()
        original_date = date.today().isoformat()

        with patch("write_obsidian_note.date") as mock_date:
            mock_date.today.return_value.isoformat.return_value = "2099-01-01"
            with pytest.raises(Exit) as exc_info:
                main(
                    video_id="abc123",
                    filename="note1",
                    tags="tag2",
                    contents="New content",
                    vault_dir=temp_vault,
                    overwrite=False,
                )
            assert exc_info.value.exit_code == 2

        current_content = (temp_vault / "note1.md").read_text()
        assert current_content == original_content

    def test_overwrite_true_updates_existing_file(self, temp_vault):
        main(
            video_id="abc123",
            filename="note2",
            tags="tag1",
            contents="Original content",
            vault_dir=temp_vault,
        )

        main(
            video_id="abc123",
            filename="note2",
            tags="tag2,tag3",
            contents="Updated content",
            vault_dir=temp_vault,
            overwrite=True,
        )

        file_path = temp_vault / "note2.md"
        content = file_path.read_text()

        assert "Updated content" in content
        assert "tag2" in content
        assert "tag3" in content

    def test_custom_frontmatter(self, temp_vault):
        main(
            video_id="abc123",
            filename="custom_fm",
            tags="test",
            contents="Content with custom frontmatter",
            frontmatter="author:John,source:YouTube",
            vault_dir=temp_vault,
        )

        file_path = temp_vault / "custom_fm.md"
        content = file_path.read_text()

        parsed = yaml.safe_load(content)
        assert parsed["author"] == "John"
        assert parsed["source"] == "YouTube"

    def test_empty_frontmatter(self, temp_vault):
        main(
            video_id="abc123",
            filename="empty_fm",
            tags="test",
            contents="Content with empty frontmatter",
            frontmatter="",
            vault_dir=temp_vault,
        )

        file_path = temp_vault / "empty_fm.md"
        assert file_path.exists()

        content = file_path.read_text()
        parsed = yaml.safe_load(content)

        assert "title" in parsed
        assert "processed_date" in parsed
        assert "tags" in parsed

    def test_frontmatter_structure(self, temp_vault):
        main(
            video_id="video123",
            filename="structured_note",
            tags="python,yaml",
            contents="Note content",
            vault_dir=temp_vault,
        )

        file_path = temp_vault / "structured_note.md"
        content = file_path.read_text()

        assert content.startswith("---")
        assert content.endswith("---")

        parsed = yaml.safe_load(content)
        assert parsed["title"] == "structured_note"
        assert parsed["processed_date"] == date.today().isoformat()
        assert isinstance(parsed["tags"], list)

    def test_tags_are_deduplicated(self, temp_vault):
        main(
            video_id="abc123",
            filename="duplicate_tags",
            tags="python,python,testing",
            contents="Content with duplicate tags",
            vault_dir=temp_vault,
        )

        file_path = temp_vault / "duplicate_tags.md"
        content = file_path.read_text()

        parsed = yaml.safe_load(content)
        python_count = parsed["tags"].count("python")
        assert python_count == 1

    def test_write_bytes_written(self, temp_vault):
        main(
            video_id="abc123",
            filename="bytes_check",
            tags="test",
            contents="Test content",
            vault_dir=temp_vault,
        )

        file_path = temp_vault / "bytes_check.md"
        assert file_path.exists()

        content = file_path.read_text()
        assert len(content) > 0
