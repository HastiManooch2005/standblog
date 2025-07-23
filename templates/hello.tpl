{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{token}}
{% endblock %}

{% block body %}
This is a text message.
{% endblock %}

{% block html %}
This is an <strong>html</strong> message.
{% endblock %}