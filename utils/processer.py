from utils.lib import *


def repeated_string(s):
    half = len(s)//2
    return s[:half] if s[half:] == s[:half] else s


# XPath selectors for each profile section
# All detail pages share the same DOM structure inside main#workspace:
#   <main#workspace> > section > ... > div > div > div[, empty, section-title, item, item, ...]
# We select item-container divs — their get_text(separator="\n") yields line-separated fields.

to_extract = {
    "main": {
        "name":        "//title",
        "description": "//h2[contains(text(), 'Acerca de') or contains(text(), 'About') or contains(text(), 'À propos')]/../following-sibling::div",
        "main_skills": "//h2[contains(text(), 'Aptitudes') or contains(text(), 'Skills') or contains(text(), 'Compétences')]/../following-sibling::div[1]",
    },
    "featured":    {"container": "//main[@id='workspace']//section//div[div[normalize-space()='Destacado' or normalize-space()='Featured']]/div[position()>2]"},
    "experience":  {"container": "//main[@id='workspace']//section//div[div[normalize-space()='Experiencia' or normalize-space()='Experience']]/div[position()>2]"},
    "education":   {"container": "//main[@id='workspace']//section//div[div[normalize-space()='Educación' or normalize-space()='Education']]/div[position()>2]"},
    "certifications": {"container": "//main[@id='workspace']//section//div[div[contains(normalize-space(), 'Licencias') or contains(normalize-space(), 'Licenses') or contains(normalize-space(), 'Certifications')]]/div[position()>2]"},
    "projects":    {"container": "//main[@id='workspace']//section//div[div[normalize-space()='Proyectos' or normalize-space()='Projects']]/div[position()>2]"},
    "courses":     {"container": "//main[@id='workspace']//section//div[div[normalize-space()='Cursos' or normalize-space()='Courses']]/div[position()>2]"},
    "languages":   {"container": "//main[@id='workspace']//section//div[div[normalize-space()='Idiomas' or normalize-space()='Languages']]/div[position()>2]"},
}

# Field counts for detail page items (lines produced by get_text(separator="\n"))
DETAIL_LAYOUT = {
    "featured":       {"title": 0, "description": 1},
    "experience":     {"basic": [0, 1, 2], "description": slice(3, None)},
    "education":      {"basic": [0, 1, 2], "description": slice(3, None)},
    "certifications": {"basic": [0, 1], "dates": [], "description": [1]},
    "projects":       {"basic": [0, 1], "description": [], "skills": []},
    "courses":        {"name": 0, "associated": 1},
    "languages":      {"languages": slice(None)},
}


def _extract_main(selector):
    """Extract main page data: name from <title>, description/skills from sections."""
    result = {}
    for key, xpath in to_extract["main"].items():
        elements = selector.xpath(xpath)
        if not elements:
            result[key] = []
            continue
        if key == "name":
            text = bs(elements[0].get(), features="lxml").get_text().strip()
            text = text.replace(" | LinkedIn", "").strip()
            result[key] = [[text]]
        else:
            texts = []
            for el in elements:
                raw = bs(el.get(), features="lxml").get_text().strip()
                lines = [repeated_string(l) for l in raw.split("\n") if l.strip()]
                heading_terms = ("Acerca de", "About", "À propos", "Aptitudes", "Skills",
                                 "Compétences", "Aptitudes (58)", "Skills (58)")
                content_lines = [l for l in lines if l not in heading_terms]
                if content_lines:
                    texts.append(content_lines)
            result[key] = texts if texts else [[]]
    return result


def _extract_detail(selector, section):
    """Extract detail page data from item container divs."""
    xpath = to_extract[section]["container"]
    elements = selector.xpath(xpath)
    if not elements:
        return {k: [] for k in DETAIL_LAYOUT[section]}

    # Extract text from each item with newline separator, skip empty items
    items = []
    for el in elements:
        text = bs(el.get(), features="lxml").get_text(separator="\n").strip()
        if not text:
            continue
        lines = [repeated_string(l.strip()) for l in text.split("\n") if l.strip()]
        if lines:
            items.append(lines)

    layout = DETAIL_LAYOUT[section]
    result = {}

    if section == "languages":
        result["languages"] = items
        return result

    if section in ("courses", "featured"):
        keys = list(layout.keys())
        idx0 = layout[keys[0]]
        idx1 = layout[keys[1]]
        result[keys[0]] = [[item[idx0]] if idx0 < len(item) else [""] for item in items]
        result[keys[1]] = [[item[idx1]] if idx1 < len(item) else [""] for item in items]
        return result

    # experience, education, certifications, projects
    for key, spec in layout.items():
        if not spec:
            result[key] = [[""] for _ in items]
        elif isinstance(spec, slice):
            # Description: join remaining fields
            desc_parts = []
            for item in items:
                desc_parts.append(item[spec])
            result[key] = desc_parts
        elif isinstance(spec, list):
            # basic: specific fields
            combined = []
            for item in items:
                combined.append([item[i] if i < len(item) else "" for i in spec])
            result[key] = combined
        else:
            result[key] = [[item[spec]] if spec < len(item) else [""] for item in items]

    # Ensure zipped lists have same length
    lengths = {k: len(v) for k, v in result.items()}
    if len(set(lengths.values())) > 1:
        max_len = max(lengths.values())
        for k, v in result.items():
            while len(v) < max_len:
                v.append(v[-1] if v else [""])

    return result


def markdownify():
    extracted = {}
    for key in to_extract:
        extracted[key] = {}
        with open(f"data/{key}.html", encoding="utf-8") as html_content:
            selector = Selector(html_content.read())
        html_content.close()

        if key == "main":
            extracted[key] = _extract_main(selector)
        else:
            extracted[key] = _extract_detail(selector, key)

    template_loader = FileSystemLoader(searchpath="./templates")
    template_env = Environment(loader=template_loader)
    template = template_env.get_template("peppermint.md")

    output_text = template.render(extracted, zip=zip, len=len)

    with open("output.md", "w", encoding="utf-8") as out:
        out.write(output_text)
