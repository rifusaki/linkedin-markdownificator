from utils.lib import *

# This dictionary contains CSS selectors for the actual content
to_extract = {"main": {"name": "body > h1",
                       "description": "body > div",
                       "location": "body > span"},
              "featured": {"title": "body > div > div.display-flex.flex-column.full-width > a.optional-action-target-wrapper.flex-1.display-flex.full-width.relative > div > div.flex-1.display-flex.flex-column > div > div.mb1 > div.display-flex > div > div > div",
                           "description": "body > div > div.display-flex.flex-column.full-width > a.optional-action-target-wrapper.flex-1.display-flex.full-width.relative > div > div.flex-1.display-flex.flex-column > div > div.display-flex > div > div > div"},
              "experience" : {"title" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > div > div > div > div",
                              "company": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(2)",
                              "date": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3)",
                              "description": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(1) > div > ul > li > div > div > div",
                              "skills": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(2) > div > ul > li > div > div > div"},
              "education" : {"institution" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > div > div > div > div",
                             "title" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > span:nth-child(2)",
                             "date" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > span.t-14.t-normal.t-black--light",
                             "skills": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(1) > div > ul > li > div > div > div"},
              "certifications": {"title": "body > div:nth-child(2) > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > div",
                                 "institution": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > span:nth-child(2)",
                                 "date": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > span:nth-child(3)",
                                 "skills": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(2) > div > ul > li > div > div > div"},
              "projects": {"title" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > div > div > div > div",
                           "date" : "body > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span",
                           "description": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(2) > div > ul > li > div > div > div",
                           "skills": "body > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li:nth-child(3) > div > ul > li > div > div > div"},
              "skills" : {"list": 0},
              "languages": {"language": "body > div > div.display-flex.flex-column.full-width.align-self-center > div > div.display-flex.flex-column.full-width > div > div > div > div",
                            "proficiency": "body > div > div.display-flex.flex-column.full-width.align-self-center > div > div.display-flex.flex-column.full-width > span"}}

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

    ## Save raw extracted data in a file        
    # with open("data/extracted.md", "w", encoding="utf-8") as f:
    #     for item in extracted.items():
    #         f.write(f"# {item[0]}\n")
    #         for subitem in item[1].items():
    #             f.write(f"## {subitem[0]}\n{subitem[1]}\n")
    #         f.write("\n")
    #     f.close

    # Load template
    template_loader = ji.FileSystemLoader(searchpath="./templates")  # Assuming templates are in the same directory
    template_env = ji.Environment(loader=template_loader)
    template = template_env.get_template("default_template.md")

    # Render and write output
    output_text = template.render(extracted)  

    with open("examples/example-default.md", "w", encoding="utf-8") as out:
        out.write(output_text)