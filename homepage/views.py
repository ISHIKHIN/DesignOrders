from django.shortcuts import render


def index(request):
    return render(request, 'homepage/index.html')


def page_not_found(request, exception):
    if hasattr(request, 'not_found_message'):
        message = request.not_found_message
    else:
        message = "Страница не найдена"

    return render(
        request,
        '404.html',
        {'message': message},
        status=404,
    )