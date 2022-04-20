from django import template

register = template.Library()


@register.filter()
def censor(value):
    badwords = ["бананы", "африке"]
    for word in badwords:
        if word in value:
            value = value.replace(word, '*' * (len(word) - 1))

    return value
