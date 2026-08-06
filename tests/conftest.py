from pathlib import Path
import pytest
from parsel import Selector
from bs4 import BeautifulSoup as bs
from utils.processer import to_extract, repeated_string, _extract_main, _extract_detail


def extract_section(section_name, base_dir=None):
    """Run the same extraction logic as markdownify for a single section."""
    if base_dir is None:
        base_dir = Path(__file__).parent / "fixtures"
    html_path = Path(base_dir) / f"{section_name}.html"
    html = html_path.read_text(encoding="utf-8")
    selector = Selector(html)

    if section_name == "main":
        return _extract_main(selector)
    else:
        return _extract_detail(selector, section_name)


@pytest.fixture
def fixture_dir():
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def extracted_main():
    return extract_section("main")


@pytest.fixture
def extracted_experience():
    return extract_section("experience")


@pytest.fixture
def extracted_education():
    return extract_section("education")


@pytest.fixture
def extracted_certifications():
    return extract_section("certifications")


@pytest.fixture
def extracted_projects():
    return extract_section("projects")


@pytest.fixture
def extracted_courses():
    return extract_section("courses")


@pytest.fixture
def extracted_languages():
    return extract_section("languages")


@pytest.fixture
def extracted_featured():
    return extract_section("featured")
