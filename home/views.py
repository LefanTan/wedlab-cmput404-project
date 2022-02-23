from django.shortcuts import redirect, render
from django.views.defaults import page_not_found
from service.models import Author, Post
from django.forms.models import model_to_dict


def auth_check_middleware(request):
    # Check if user is authenticated and also check if the user is an Author

    if not request.user.is_authenticated:
        return (redirect('login'), False)

    try:
        author = Author.objects.get(user=request.user.id)
    except Exception as e:
        return (page_not_found(request, e), False)
    return (author, True)


def home(request):
    author, success = auth_check_middleware(request)

    try:
        pass
    except Exception as e:
        pass

    if success:
        return render(request, 'home.html', model_to_dict(author))
    return author


def post_create(request):
    author, success = auth_check_middleware(request)

    if success:
        if request.method == 'GET':
            return render(request, 'post_form.html', context={"author": model_to_dict(author), "name": request.resolver_match.url_name})
    return author


def post_edit(request, post_pk):
    author, success = auth_check_middleware(request)

    # Get Post object that we want to edit, only allow post made by author
    try:
        post = Post.objects.get(pk=post_pk, author=author.id)
    except Exception as e:
        return page_not_found(request, e)

    if success:
        if request.method == 'GET':
            return render(request, 'post_form.html', context={"author": model_to_dict(author), "post": model_to_dict(post), "name": request.resolver_match.url_name})
    return author
