{% for index in main.name %}
# {{main.name[loop.index0]}}
> {{main.description[loop.index0]}}

{{main.location[loop.index0]}}
{% endfor %}

## Featured
{% for index in featured.title %}
### {{featured.title[loop.index0]}}
{{featured.description[loop.index0]}}
{%endfor%}

## Experience
{% for index in experience.title %}
### {{experience.title[loop.index0]}}
> {{experience.company[loop.index0]}} - {{experience.date[loop.index0]}}

{{experience.description[loop.index0]}}
###### {{experience.skills[loop.index0]}}
{%endfor%}

## Education
{% for index in education.title %}
### {{education.title[loop.index0]}}
> {{education.institution[loop.index0]}}

{{education.date[loop.index0]}}
###### {{education.skills[loop.index0]}}
{%endfor%}

## Certifications
{% for index in certifications.title %}
### {{certifications.title[loop.index0]}} - {{certifications.institution[loop.index0]}}
> {{certifications.date[loop.index0]}}
###### {{certifications.skills[loop.index0]}}
{%endfor%}

## Projects
{% for index in projects.title %}
### {{projects.title[loop.index0]}}
> {{projects.date[loop.index0]}}

{{projects.description[loop.index0]}}
###### {{certifications.skills[loop.index0]}}
{%endfor%}

## Skills
> [!NOTE]
> Pending

## Languages
{% for index in languages.language %}
- **{{languages.language[loop.index0]}}**
  - {{languages.proficiency[loop.index0]}}
{%endfor%}