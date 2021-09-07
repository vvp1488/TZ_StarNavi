from .models import UserActivity
from django.utils import timezone


def last_request_user_middleware(get_response):

    def middleware(request):
        response = get_response(request)

        if request.user.is_authenticated:
            UserActivity.objects.filter(user=request.user).update(user_last_request=f'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}, тип запроса-{request.method}')

        return response

    return middleware


