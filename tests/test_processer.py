from pathlib import Path
import pytest
from parsel import Selector
from bs4 import BeautifulSoup as bs
from utils.processer import to_extract, repeated_string
from tests.conftest import extract_section


# ── helpers ──────────────────────────────────────────────────────────────────

def xpath_entries():
    """Flatten to_extract into (section, key, xpath) triples for presence testing."""
    for section, selectors in to_extract.items():
        for key, xpath in selectors.items():
            yield pytest.param(section, key, xpath, id=f"{section}/{key}")


# ── XPath presence (each XPath must return ≥1 match against real HTML) ───────

# Sections that legitimately have 0 items when the profile is empty
EMPTY_OK_SECTIONS = {"featured"}


@pytest.mark.parametrize("section,key,xpath", list(xpath_entries()))
def test_every_xpath_matches_at_least_one_element(section, key, xpath, fixture_dir):
    """Each XPath must return ≥1 match against the real LinkedIn HTML fixture."""
    html_path = fixture_dir / f"{section}.html"
    html = html_path.read_text(encoding="utf-8")
    selector = Selector(html)

    results = selector.xpath(xpath)
    if section in EMPTY_OK_SECTIONS and len(results) == 0:
        pytest.skip(f"[{section}/{key}] profile has no items in this section")
    assert len(results) >= 1, (
        f"[{section}/{key}] XPath matched 0 elements — LinkedIn layout may have changed.\n"
        f"  XPath: {xpath}"
    )


# ── extracted data shape tests ───────────────────────────────────────────────

def test_main_name_is_nonempty(extracted_main):
    names = extracted_main["name"]
    assert len(names) >= 1, "main/name: no matches"
    assert len(names[0]) >= 1, "main/name: first match has no content"
    assert names[0][0], "main/name: first line is empty"


def test_main_description_is_nonempty(extracted_main):
    desc = extracted_main["description"]
    assert len(desc) >= 1, "main/description: no matches"


def test_main_skills_are_nonempty(extracted_main):
    skills = extracted_main["main_skills"]
    assert len(skills) >= 1, "main/main_skills: no matches"


def test_main_fields_have_same_length(extracted_main):
    """name, description, main_skills must align for zip() in templates."""
    n_name = len(extracted_main["name"])
    n_desc = len(extracted_main["description"])
    n_skills = len(extracted_main["main_skills"])
    assert n_name == n_desc == n_skills, (
        f"zip() will silently drop data: name={n_name}, "
        f"description={n_desc}, skills={n_skills}"
    )


def test_experience_basic_has_three_parts(extracted_experience):
    """Each basic entry splits into ≥3 lines: role, company, dates."""
    for i, entry in enumerate(extracted_experience["basic"]):
        assert len(entry) >= 3, (
            f"experience/basic[{i}]: expected ≥3 parts (role/company/dates), got {entry}"
        )


def test_experience_has_description_for_each_basic(extracted_experience):
    assert len(extracted_experience["basic"]) == len(extracted_experience["description"]), (
        "basic and description must have same length for zip()"
    )


def test_experience_description_each_has_text(extracted_experience):
    for i, entry in enumerate(extracted_experience["description"]):
        assert len(entry) >= 1, f"experience/description[{i}]: empty"


def test_education_basic_has_three_parts(extracted_education):
    """Each basic entry splits into ≥3 lines: school, degree, dates."""
    for i, entry in enumerate(extracted_education["basic"]):
        assert len(entry) >= 3, (
            f"education/basic[{i}]: expected ≥3 parts, got {entry}"
        )


def test_education_basic_description_same_length(extracted_education):
    assert len(extracted_education["basic"]) == len(extracted_education["description"]), (
        "basic and description must have same length for zip()"
    )


def test_certifications_basic_is_nonempty(extracted_certifications):
    for i, entry in enumerate(extracted_certifications["basic"]):
        assert len(entry) >= 1, f"certifications/basic[{i}]: empty"
        assert entry[0].strip(), f"certifications/basic[{i}]: whitespace only"


def test_certifications_basic_description_same_length(extracted_certifications):
    assert len(extracted_certifications["basic"]) == len(extracted_certifications["description"]), (
        "basic and description must have same length for zip()"
    )


def test_projects_basic_is_nonempty(extracted_projects):
    for i, entry in enumerate(extracted_projects["basic"]):
        assert len(entry) >= 1, f"projects/basic[{i}]: empty"
        assert entry[0].strip(), f"projects/basic[{i}]: whitespace only"


def test_projects_zips_same_length(extracted_projects):
    assert len(extracted_projects["basic"]) == len(extracted_projects["description"]) == len(extracted_projects["skills"]), (
        "basic, description, skills must have same length for zip()"
    )


def test_courses_name_is_nonempty(extracted_courses):
    for i, entry in enumerate(extracted_courses["name"]):
        assert len(entry) >= 1, f"courses/name[{i}]: empty"
        assert entry[0].strip(), f"courses/name[{i}]: whitespace only"


def test_courses_associated_is_nonempty(extracted_courses):
    for i, entry in enumerate(extracted_courses["associated"]):
        assert len(entry) >= 1, f"courses/associated[{i}]: empty"


def test_courses_name_associated_same_length(extracted_courses):
    assert len(extracted_courses["name"]) == len(extracted_courses["associated"]), (
        "name and associated must have same length for zip()"
    )


def test_languages_has_two_parts(extracted_languages):
    """Each language entry: [name, proficiency]."""
    for i, entry in enumerate(extracted_languages["languages"]):
        assert len(entry) >= 2, (
            f"languages[{i}]: expected ≥2 parts (name, proficiency), got {entry}"
        )


def test_featured_title_is_nonempty(extracted_featured):
    for i, entry in enumerate(extracted_featured.get("title", [])):
        assert len(entry) >= 1, f"featured/title[{i}]: empty"


def test_featured_description_is_nonempty(extracted_featured):
    for i, entry in enumerate(extracted_featured.get("description", [])):
        assert len(entry) >= 1, f"featured/description[{i}]: empty"


def test_featured_title_description_same_length(extracted_featured):
    assert len(extracted_featured.get("title", [])) == len(extracted_featured.get("description", [])), (
        "title and description must have same length for zip()"
    )


# ── HTML-to-text extraction ──────────────────────────────────────────────────

def test_bs_extracts_text_from_nested_spans():
    html = "<div><span>Hello</span><span>World</span></div>"
    text = bs(html, features="lxml").get_text().strip()
    assert text == "HelloWorld"


def test_bs_get_text_no_separator_concatenates_inline():
    html = "<div><div>Role</div><div>Company</div><div>Dates</div></div>"
    text = bs(html, features="lxml").get_text().strip()
    assert text == "RoleCompanyDates"


def test_bs_newlines_from_source_whitespace_are_preserved():
    html = "<div>\n<div>Role</div>\n<div>Company</div>\n<div>Dates</div>\n</div>"
    text = bs(html, features="lxml").get_text().strip()
    parts = [p for p in text.split("\n") if p.strip()]
    assert parts == ["Role", "Company", "Dates"]


def test_bs_get_text_with_separator_adds_newlines():
    html = "<div><div>Role</div><div>Company</div><div>Dates</div></div>"
    text = bs(html, features="lxml").get_text(separator="\n").strip()
    parts = [p for p in text.split("\n") if p.strip()]
    assert parts == ["Role", "Company", "Dates"]


def test_bs_preserves_text_inside_anchors():
    html = '<a href="#"><div>School Name</div><span>Degree</span></a>'
    text = bs(html, features="lxml").get_text(separator="\n").strip()
    assert "School Name" in text
    assert "Degree" in text


def test_bs_handles_unordered_lists():
    html = "<ul><li>Item One</li><li>Item Two</li></ul>"
    text = bs(html, features="lxml").get_text().strip()
    assert "Item One" in text
    assert "Item Two" in text


def test_repeated_string_deduplicates():
    assert repeated_string("hellohello") == "hello"
    assert repeated_string("abcabc") == "abc"
    assert repeated_string("xx") == "x"


def test_repeated_string_leaves_nonduplicate_intact():
    assert repeated_string("hello") == "hello"
    assert repeated_string("abcde") == "abcde"


def test_repeated_string_handles_empty():
    assert repeated_string("") == ""


def test_repeated_string_handles_single_char():
    assert repeated_string("a") == "a"


def test_parsel_xpath_getall_returns_strings():
    html = '<div class="a"><span>text</span></div>'
    sel = Selector(text=html)
    results = sel.xpath("//div[@class='a']").getall()
    assert len(results) == 1
    assert isinstance(results[0], str)
    assert "text" in results[0]
