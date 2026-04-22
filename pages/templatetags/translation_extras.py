from django import template
from django.utils import translation

register = template.Library()


@register.filter
def trans_field(obj, field_name):
    """
    Возвращает значение поля на текущем языке.
    Использование: {{ hero|trans_field:"title" }}
    """
    if obj is None:
        return ''
    
    lang = translation.get_language()
    
    # Для русского возвращаем базовое поле
    if lang == 'ru':
        return getattr(obj, field_name, '')
    
    # Для остальных языков ищем поле с суффиксом
    if lang == 'zh-hans':
        lang_field = f"{field_name}_zh_hans"
    else:
        lang_field = f"{field_name}_{lang}"
    
    # Получаем значение, если пустое - возвращаем русский
    value = getattr(obj, lang_field, '')
    if value:
        return value
    return getattr(obj, field_name, '')


@register.simple_tag
def get_trans_field(obj, field_name):
    """
    Тег для получения переведенного поля.
    Использование: {% get_trans_field room "name" %}
    """
    if obj is None:
        return ''
    
    lang = translation.get_language()
    
    if lang == 'ru':
        return getattr(obj, field_name, '')
    
    if lang == 'zh-hans':
        lang_field = f"{field_name}_zh_hans"
    else:
        lang_field = f"{field_name}_{lang}"
    
    value = getattr(obj, lang_field, '')
    if value:
        return value
    return getattr(obj, field_name, '')


@register.filter
def trans_text(text):
    """
    Фильтр для перевода статического текста через Google Translate.
    В реальном проекте здесь должен быть вызов к API.
    """
    return text
