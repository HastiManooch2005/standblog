{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{token}}
{% endblock %}

{% block body %}
This is a text message.
{% endblock %}

{% block html %}
http://127.0.0.1:8000/api/v1/activation/token/{{token}}
{% endblock %}