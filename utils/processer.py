from utils.lib import *

def repeated_string(s):
    half = len(s)//2
    return s[:half] if s[half:] == s[:half] else s


# This dictionary contains CSS selectors for the actual content
to_extract = {
                "main": {"name": "h1",
                         "summary": "div > div.scaffold-layout.scaffold-layout--breakpoint-xl.scaffold-layout--main-aside.scaffold-layout--reflow.pv-profile.pvs-loader-wrapper__shimmer--animate > div > div > main > section.artdeco-card.PTRpMUClrkHGHqOEdVoDPGetewwGdXI > div.ph5 > div.mt2.relative > div:nth-child(1) > div.text-body-medium.break-words",
                       "description": "div > div.scaffold-layout.scaffold-layout--breakpoint-xl.scaffold-layout--main-aside.scaffold-layout--reflow.pv-profile.pvs-loader-wrapper__shimmer--animate > div > div > main > section:nth-child(4) > div.display-flex.ph5.pv3 > div",
                       "main_skills": "div > div.scaffold-layout.scaffold-layout--breakpoint-xl.scaffold-layout--main-aside.scaffold-layout--reflow.pv-profile.pvs-loader-wrapper__shimmer--animate > div > div > main > section:nth-child(4) > div:nth-child(4) > div > ul > li > div > div > div.display-flex.flex-column.full-width.align-self-center > div > div.display-flex.flex-column.full-width > div:nth-child(2)"},
              "featured": {"title": "div > div > div.display-flex.flex-column.full-width > a.optional-action-target-wrapper.flex-1.display-flex.full-width.relative > div > div.flex-1.display-flex.flex-column > div > div.mb1 > div.display-flex",
                           "description": "div > div > div.display-flex.flex-column.full-width > a.optional-action-target-wrapper.flex-1.display-flex.full-width.relative > div > div.flex-1.display-flex.flex-column > div > div.display-flex"},
              "experience" : {"basic" : "div > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between",
                              "description": "div > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components"},
              "education" : {"basic" : "div > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between",
                             "description": "div > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components"},
              "certifications": {"basic": "div > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between",
                                 "skills": "div > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li > div > ul"},
              "courses": {"name": "div > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > div",
                          "associated": "div > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components > ul > li > div > div > div.display-flex"},
              "projects": {"basic" : "div > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width",
                           "description": "div > div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container.pvs-entity__sub-components"},
              "languages": {"languages": "div > div > div.display-flex.flex-column.full-width.align-self-center > div > div.display-flex.flex-column.full-width"}
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

    # # Load template
    # template_loader = ji.FileSystemLoader(searchpath="./templates")  # Assuming templates are in the same directory
    # template_env = ji.Environment(loader=template_loader)
    # template = template_env.get_template("default_template.md")

    # # Render and write output
    # output_text = template.render(extracted)  

    # with open("output.md", "w", encoding="utf-8") as out:
    #     out.write(output_text)
