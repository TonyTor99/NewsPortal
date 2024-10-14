from django import template
import re


register = template.Library()


@register.filter()
def censor(value):
    try:
        def replace_with_stars(match):
            word = match.group(0)
            return f'{word[0]}{(int(len(word)) - 1) * '*'}'

        # Регулярное выражение для поиска слов, начинающихся с заглавной буквы
        censored_text = re.sub(r'\b[A-ZА-Я][a-zа-яё]*\b', replace_with_stars, value)

        return censored_text
    except TypeError:
        print('Введены данные не в формате текста')
