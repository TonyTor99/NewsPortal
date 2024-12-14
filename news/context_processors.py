from django.utils.timezone import get_current_timezone, localtime, now
import pytz


def timezone_context(request):
    return {
        'current_timezone': str(get_current_timezone()),  # Текущий часовой пояс
        'timezones': pytz.common_timezones,  # Все доступные часовые пояса
        'current_time': localtime(now()) # Время сейчас
    }
