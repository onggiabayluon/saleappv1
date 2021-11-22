# How to use component, For Example: 

{% from "components/card.html" import card with context %}
{{ card(
    image='test',
    name='test',
    description='test',
    price='test'
) }}