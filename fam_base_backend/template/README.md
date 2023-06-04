# {{ project_name|replace('_', ' ')|replace('-', ' ') }}

## {% if project_license != 'none' %}LICENSE{% endif %}

{% if project_license != 'none' %}This project is licensed under the terms of the {{project_license}}.{% endif %}
