from django import template
import re

from news.templatetags.forbidden_words import forbidden_words


register = template.Library()


# @register.filter()
# def censor(value):
#     try:
#         def replace_with_stars(match):
#             word = match.group(0)
#             return f'{word[0]}{(int(len(word)) - 1) * '*'}'
#
#         # Регулярное выражение для поиска слов, начинающихся с заглавной буквы
#         censored_text = re.sub(r'\b[A-ZА-Я][a-zа-яё]*\b', replace_with_stars, value)
#
#         return censored_text
#     except TypeError:
#         print('Введены данные не в формате текста')


@register.filter()
def censor(value):
    words = value.split()
    consed_text = []
    for word in words:
        if word in forbidden_words:
            consed_text.append('*' + word[1:-1] + '*')
        else:
            consed_text.append(word)
    return ' '.join(consed_text)
