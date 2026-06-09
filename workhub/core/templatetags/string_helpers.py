from django import template

register = template.Library()

@register.filter
def convert_link_to_shortlink(text):
    """Конвертирует ссылки в слово 'ссылка' """
    words = text.split(" ")
    result = ""

    for word in words:
        if word.startswith("http") or word.startswith("https"):
            result += ' <a target="_blank" href="' + word + '">Ссылка.</a> '
        else:
            result += word + ' '
    return result
