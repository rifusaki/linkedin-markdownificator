{% for name, description, skills in zip(main.name, main.description, main.main_skills) %}
---
title: CV - {{ name[0] }}
layout: single
permalink: /CV/
author_profile: true
---
{{ description[0] }}
*{{skills[0]}}*
{% endfor %}

## Featured
{% for title, description in zip(featured.title, featured.description) %}
### {{title[0]}}
{{description[0]}}

{% endfor %}

## Experience
{% for basic, description in zip(experience.basic, experience.description) %}
<h3>{{basic[0]}} - {{basic[1]}}</h3>
<p align="right"><i>{{basic[2]}}</i></p>

{{description[0]}}\
<small>{{description[1]}}</small>

{% endfor %}

## Education
{% for basic, description in zip(education.basic, education.description) %}
<h3>{{basic[1]}} - {{basic[0]}}</h3>
<p align="right"><i>{{basic[2]}}</i></p>\

{% if len(description) > 1%}
{{description[0]}}
{% if len(description) > 2 %}
{{description[1]}}
{% endif %}
{% endif %}
<small>{{description[-1]}}</small>

{% endfor %}

## Certifications
{% for basic, description in zip(certifications.basic, certifications.description) %}
### {{basic[0]}}
<p> <span style="float:left;"><b>{{basic[1]}}</b></span> <span style="float:right;"><i>{{basic[2]}}</i></span> </p>\
<small>{{description[0]}}</small>

{% endfor %}

## Projects
{% for basic, description, skills in zip(projects.basic, projects.description, projects.skills) %}
### {{basic[0]}}
<p align="right"><i>{{basic[1]}}</i></p>

{{description[0]}}
<small>{{skills[0]}}</small>

{%endfor%}

## Courses
{% for name, associated in zip(courses.name, courses.associated) %}
### {{name[0]}}
<p align="right"><small>{{associated[0]}}</small></p>

{% endfor %}

## Languages
{% for language in languages.languages %}
- **{{language[0]}}:** {{language[1]}}
{% endfor %}