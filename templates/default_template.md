{% for name, summary, description, skills in zip(main.name, main.summary, main.description, main.main_skills) %}
# {{ name[0] }} 
{% if summary %} 
    > {{ summary[0] }}
{% endif %}
{% if description %}
{{ description[0] }}
{% endif %}
{% if skills %}
###### {{ skills[0] }}
{% endif %}
{% endfor %}

## Featured
{% for title, description in zip(featured.title, featured.description) %}
### {{title[0]}}
{{description[0]}}
{% endfor %}

## Experience
{% for basic, description in zip(experience.basic, experience.description) %}
### {{basic[0]}} - {{basic[1]}}
> {{basic[2]}}

{{description[0]}}

###### {{description[1]}}
{% endfor %}

## Education
{% for basic, description in zip(education.basic, education.description) %}
### {{basic[1]}}
> {{basic[0]}} - {{basic[2]}}

{% if len(description) > 1%}
{{description[0]}}
{% if len(description) > 2 %}
{{description[1]}}
{% endif %}
{% endif %}
###### {{description[-1]}}
{% endfor %}

## Certifications
{% for basic, description in zip(certifications.basic, certifications.description) %}
### {{basic[0]}}
> {{basic[1]}} - {{basic[2]}}

{{description[0]}}
{% endfor %}

## Projects
{% for basic, description in zip(projects.basic, projects.description) %}
### {{basic[0]}}
> {{basic[1]}} - {{description[0]}}

{{description[1]}}
###### {{description[-1]}}
{%endfor%}

## Courses
{% for name, associated in zip(courses.name, courses.associated) %}
### {{name[0]}}
> {{associated[0]}}
{% endfor %}

## Languages
{% for language in languages.languages %}
- **{{language[0]}}**
  - {{language[1]}}
{% endfor %}