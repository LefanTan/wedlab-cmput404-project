import base64
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.views.defaults import page_not_found
from service.models import Author, Host, Post, FollowRequest, InboxObject, Comment
from service.serializers import PostSerializer, FollowRequestSerializer
from django.forms.models import model_to_dict
from requests import get


def auth_check_middleware(request):
    # Check if user is authenticated and also check if the user is an Author

    if not request.user.is_authenticated:
        return (redirect('login'), False)

    try:
        author = Author.objects.get(user=request.user.id)
    except Exception as e:
        return (redirect('login'), False)
    return (author, True)


def home(request):
    author, success = auth_check_middleware(request)
    item = None
    try:
        item = InboxObject.objects.get(author=author)
    except Exception as e:
        pass

    # TODO: Use posts that has arrived in user's Inbox
    try:
        hosts = Host.objects.filter(allowed=True)
        other_posts = []

        for host in hosts:
            get_authors_url = host.url + 'authors/'
            encoded_basic = base64.b64encode(
                bytes(f'{host.name}:{host.password}', 'utf-8')).decode('utf-8')
            headers = {'Authorization': f'Basic {encoded_basic}'}
            result = get(get_authors_url, headers=headers).json()
            other_authors = result.get('items')
            for other_author in other_authors:
                other_author_id = other_author.get('id').split('/')[-1]
                author_posts_url = f"{get_authors_url}{other_author_id}/posts"
                posts_result = get(author_posts_url, headers=headers).json()
                if posts_result.get('items'):
                    other_posts += posts_result.get('items')

        page_number = request.GET.get('page') or 1
        size = request.GET.get('size') or 5

        post_objs = Post.objects.filter(
            visibility="PUBLIC", unlisted=False).order_by('-publishedDate')

        paginator = Paginator(post_objs, size)
        posts = paginator.get_page(page_number).object_list

        postsData = PostSerializer(posts, many=True).data #+ other_posts

    except Exception as e:
        print(e)

    if success:
        return render(request, 'home.html', {"author": model_to_dict(author), "item": item, "posts": postsData})
    return author


def post_list(request, author_pk):
    # Show a list of post made by author_pk

    author, success = auth_check_middleware(request)

    try:
        # Get public and listed posts for other profiles
        if author_pk == author.id:
            posts = author.post_set.all().order_by('-publishedDate')
        else:
            posts = Post.objects.filter(
                author=author_pk, unlisted=False, visibility='PUBLIC')

        postsData = PostSerializer(posts, many=True).data
    except Exception as e:
        return page_not_found(request, e)

    if success:
        if request.method == 'GET':
            return render(request, 'post_list.html',
                          {"author": model_to_dict(author), "posts": postsData, "edit": author_pk == author.id})
    return author


def follow_request(request):
    author, success = auth_check_middleware(request)

    if success:
        if request.method == 'GET':
            return render(request, 'followrequest_form.html',
                          context={"author": model_to_dict(author), "name": request.resolver_match.url_name})
    return author


def post_create(request):
    author, success = auth_check_middleware(request)

    if success:
        if request.method == 'GET':
            return render(request, 'post_form.html',
                          context={"author": model_to_dict(author), "name": request.resolver_match.url_name})
    return author


def messages(request):
    author, success = auth_check_middleware(request)
    item = None
    posts = []

    try:
        item = InboxObject.objects.all()
        comments = Comment.objects.all()

        # Store all requests into a list
        for i in item:
            if i.author_id == author.id:
                if i.content_type.model_class() is Post:
                    posts.append(Post.objects.get(id=i.object_id))

    except Exception as e:
        pass

    if success:
        if request.method == 'GET':
            return render(request, 'messages.html',
                          context={"author": model_to_dict(author), "item": item, "posts": posts, "comments": comments,
                                   "name": request.resolver_match.url_name})
    return author


def requests(request):
    author, success = auth_check_middleware(request)
    item = None
    followRequests = []

    try:
        item = InboxObject.objects.all()

        # Store all requests into a list
        for i in item:
            if i.author_id == author.id:
                if i.content_type.model_class() is FollowRequest:
                    followRequests.append(
                        FollowRequest.objects.get(id=i.object_id))

    except Exception as e:
        pass

    if success:
        if request.method == 'GET':
            return render(request, 'requests.html',
                          context={"author": model_to_dict(author), "item": item, "content": followRequests,
                                   "name": request.resolver_match.url_name})
    return author


def post_edit(request, post_pk):
    # IN PROGRESS
    author, success = auth_check_middleware(request)

    # Get Post object that we want to edit, only allow post made by author
    try:
        post = Post.objects.get(pk=post_pk, author=author.id)
        postData = PostSerializer(post).data
    except Exception as e:
        return page_not_found(request, e)

    if success:
        if request.method == 'GET':
            return render(request, 'post_form.html', context={"author": model_to_dict(author), "post": postData,
                                                              "name": request.resolver_match.url_name})
    return author


def profile(request, author_pk):
    # Show author's profile
    author, success = auth_check_middleware(request)

    try:
        request_author = Author.objects.get(pk=author_pk)
    except Exception as e:
        return page_not_found(request, e)

    if success:
        if request.method == 'GET':
            return render(request, 'profile.html',
                          context={"author": model_to_dict(request_author), "name": request.resolver_match.url_name,
                                   "edit": author.id == author_pk, "error": request.GET.get('error')})
    return author


def share_post(request, post_pk):
    # Show author's profile
    author, success = auth_check_middleware(request)
    post = Post.objects.get(pk=post_pk)
    postData = PostSerializer(post).data
    allAuthors = Author.objects.all()
    if success:
        if request.method == 'GET':
            return render(request, 'sharepost.html', context={"requesting_author": model_to_dict(author), "post": postData, "allauthors": allAuthors})
    return author
