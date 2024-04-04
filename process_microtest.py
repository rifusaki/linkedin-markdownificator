from utils.lib import *

## This is for testing the CSS selectors for stage 2
def repeated_string(s):
    half = len(s)//2
    return s[:half] if s[half:] == s[:half] else s

with open("data/certifications.html", encoding="utf-8") as html_content:
    selector = Selector(html_content.read())
html_content.close()

res = selector.css("div > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between").getall()

print(len(res))

for i in range(len(res)):
    text = bs(res[i], features="lxml").get_text().strip()
    res[i] = text.split('\n')
    res[i] = [repeated_string(item) for item in res[i] if item.strip()]

print(res)
