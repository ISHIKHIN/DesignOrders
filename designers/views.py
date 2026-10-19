from django.http import Http404
from django.shortcuts import render

from storage import load_designers


def designer_list(request):
    designers = load_designers()
    return render(
        request,
        'designers/designer_list.html',
        {'designers': designers.values()},
    )


def designer_detail(request, designer_id):
    designers = load_designers()
    designer = designers.get(designer_id)
    if designer is None:
        raise Http404("Дизайнер не найден")
    return render(
        request,
        'designers/designer_detail.html',
        {'designer': designer},
    )