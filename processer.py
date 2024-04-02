from lib import *

# This dictionary contains CSS selectors for the actual content
to_extract = {"projects": {"title" : 0,
                          "content": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li > div > ul > li > div > div > div",
                          "links": 0}}

def repeated_string(s):
    half = len(s)//2
    return s[:half] if s[half:] == s[:half] else s

def markdownify():
    extracted = {}
    for key in list(to_extract.keys()):
        extracted[key] = {}
        with open(f"data/{key}.html", encoding="utf-8") as html_content:
            selector = Selector(html_content.read())
        html_content.close()

        for item in to_extract[key].items():
            if type(item[1]) == str:
                res = selector.css(item[1]).getall()
                for index in range(len(res)):
                    text = bs(res[index], features="lxml").get_text().strip()
                    res[index] = repeated_string(text)
                extracted[key] |= {item[0]: res}
            
    return extracted

extracted = markdownify()

with open("data/extracted.md", "w", encoding="utf-8") as f:
    for item in extracted.items():
        f.write(f"# {item[0]}\n")
        for subitem in item[1].items():
            f.write(f"## {subitem[0]}\n{subitem[1]}")
f.close