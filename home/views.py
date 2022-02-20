from django.shortcuts import redirect, render

from service.models import Author
from django.forms.models import model_to_dict


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        author = Author.objects.get(user=request.user.id)
    except Exception as e:
        pass
    return render(request, 'home.html', model_to_dict(author))
