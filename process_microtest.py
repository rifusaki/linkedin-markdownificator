from utils.lib import *


def repeated_string(s):
    half = len(s)//2
    return s[:half] if s[half:] == s[:half] else s


## Single CSS selector testing
# with open("data/certifications.html", encoding="utf-8") as html_content:
#     selector = Selector(html_content.read())
# html_content.close()
# res = selector.css("div > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li > div > ul").getall()

# for index in range(len(res)):
#     text = bs(res[index], features="lxml").get_text().strip()
#     res[index] = text.split('\n')
#     res[index] = [repeated_string(item) for item in res[index] if item.strip()]
# print(res)


## Bulk testing (processer.py)
to_extract = {
                # "main": {"name": "body > h1",
                #        "description": "body > div",
                #        "location": "body > span"},
            #   "featured": {"title": "body > div > div.display-flex.flex-column.full-width > a.optional-action-target-wrapper.flex-1.display-flex.full-width.relative > div > div.flex-1.display-flex.flex-column > div > div.mb1 > div.display-flex > div > div > div",
            #                "description": "body > div > div.display-flex.flex-column.full-width > a.optional-action-target-wrapper.flex-1.display-flex.full-width.relative > div > div.flex-1.display-flex.flex-column > div > div.display-flex > div > div > div"},
            #   "experience" : {"title" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > div > div > div > div",
            #                   "company": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(2)",
            #                   "date": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3)",
            #                   "description": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(1) > div > ul > li > div > div > div",
            #                   "skills": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(2) > div > ul > li > div > div > div"},
            #   "education" : {"institution" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > div > div > div > div",
            #                  "title" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > span:nth-child(2)",
            #                  "date" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > span.t-14.t-normal.t-black--light",
            #                  "skills": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(1) > div > ul > li > div > div > div"},
              "certifications": {"basic": "div > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between",
                                 "skills": "div > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li > div > ul"},
            #   "projects": {"title" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > div > div > div > div",
            #                "date" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span",
            #                "description": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(2) > div > ul > li > div > div > div",
            #                "skills": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(3) > div > ul > li > div > div > div"},
            #   "languages": {"language": "body > div > div.display-flex.flex-column.full-width.align-self-center > div > div.display-flex.flex-column.full-width > div > div > div > div",
            #                 "proficiency": "body > div > div.display-flex.flex-column.full-width.align-self-center > div > div.display-flex.flex-column.full-width > span"},
              "skills" : {"list": 0}
                            }


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
                    res[index] = text.split('\n')
                    res[index] = [repeated_string(item) for item in res[index] if item.strip()]
                extracted[key] |= {item[0]: res}

    # Save raw extracted data in a file        
    with open("data/extracted.md", "w", encoding="utf-8") as f:
        for item in extracted.items():
            f.write(f"# {item[0]}\n")
            for subitem in item[1].items():
                f.write(f"## {subitem[0]}\n{subitem[1]}\n")
            f.write("\n")
        f.close

markdownify()