from django import template
from django.utils import translation

register = template.Library()

# Словарь статических переводов
STATIC_TRANSLATIONS = {
    'ru': {
        'Welcome to Dobroslawa': 'Добро пожаловать в Доброславию',
        'Cozy rooms in the heart of Rostov-on-Don': 'Уютные номера в сердце Ростова-на-Дону',
        'Check-in': 'Заезд',
        'Check-out': 'Выезд', 
        'Guests': 'Гости',
        'guest': 'гость',
        'guests': 'гостей',
        'Check Availability': 'Проверить наличие',
        'Scroll down': 'Прокрутите вниз',
        'Our Rooms': 'Наши номера',
        'Comfortable accommodation for every taste': 'Комфортное размещение на любой вкус',
        'Photo coming soon': 'Фото скоро будет',
        'night': 'ночь',
        'Capacity': 'Вместимость',
        'Area': 'Площадь',
        'Wi-Fi': 'Wi-Fi',
        'Air conditioning': 'Кондиционер',
        'TV': 'Телевизор',
        'View Details': 'Подробнее',
        'Why Choose Us': 'Почему выбирают нас',
        'Everything for your comfortable stay': 'Всё для вашего комфортного проживания',
        'Guest Reviews': 'Отзывы гостей',
        'What our guests say about us': 'Что говорят о нас гости',
        'Ready to book your stay?': 'Готовы забронировать?',
        'Contact us now and get the best price guarantee': 'Свяжитесь с нами и получите гарантию лучшей цены',
        'Book Online': 'Забронировать',
        'About': 'О нас',
        'Contacts': 'Контакты',
        'House Rules': 'Порядок проживания',
        'Everything you need to know for a comfortable stay': 'Всё, что нужно знать для комфортного проживания',
    },
    'zh-hans': {
        'Welcome to Dobroslawa': '欢迎来到多布罗斯拉维亚',
        'Cozy rooms in the heart of Rostov-on-Don': '位于顿河畔罗斯托夫市中心的舒适客房',
        'Check-in': '入住',
        'Check-out': '退房',
        'Guests': '客人',
        'guest': '位客人',
        'guests': '位客人',
        'Check Availability': '查询可用性',
        'Scroll down': '向下滚动',
        'Our Rooms': '我们的客房',
        'Comfortable accommodation for every taste': '适合各种口味的舒适住宿',
        'Photo coming soon': '照片即将上线',
        'night': '/晚',
        'Capacity': '容量',
        'Area': '面积',
        'Wi-Fi': '无线网络',
        'Air conditioning': '空调',
        'TV': '电视',
        'View Details': '查看详情',
        'Why Choose Us': '为什么选择我们',
        'Everything for your comfortable stay': '为您提供舒适住宿的一切',
        'Guest Reviews': '客人评价',
        'What our guests say about us': '客人对我们的评价',
        'Ready to book your stay?': '准备好预订您的住宿了吗？',
        'Contact us now and get the best price guarantee': '立即联系我们，获取最优惠价格保证',
        'Book Online': '在线预订',
        'About': '关于我们',
        'Contacts': '联系我们',
        'House Rules': '住宿规定',
        'Everything you need to know for a comfortable stay': '舒适住宿须知',
    }
}

@register.simple_tag
def static_trans(text):
    """
    Простой тег для статических переводов.
    Использование: {% static_trans "Check-in" %}
    """
    lang = translation.get_language()
    if lang == 'ru':
        return STATIC_TRANSLATIONS['ru'].get(text, text)
    elif lang == 'zh-hans':
        return STATIC_TRANSLATIONS['zh-hans'].get(text, text)
    return text
