"""
Контекстный процессор для передачи языка пользователя в шаблоны.
Читает язык из cookies и передает его в контекст всех шаблонов.
"""


def user_language(request):
    """
    Возвращает язык пользователя из cookies.
    Если cookie не установлен, возвращает 'RU' по умолчанию.
    """
    language = request.COOKIES.get('lang', 'RU')
    # Валидация: если язык не RU или EN, возвращаем RU
    if language not in ['RU', 'EN']:
        language = 'RU'
    return {'user_language': language}

