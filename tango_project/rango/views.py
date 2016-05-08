
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Category, Page, UserProfile, User
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .bing_search import run_query
from .my_random_generate import generate
from django.template.defaultfilters import slugify
from django.utils.html import escape


def my_image(request):
    image_data = open("./static/images/favicon.ico", "rb").read()
    print("open")
    return HttpResponse(image_data, content_type="image/png")


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rank/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            # return HttpResponse("Invalid login details supplied.")
            return render(request, 'rango/login.html', {'message': "Invalid login details supplied."})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})


def register(request):

    # if request.session.test_cookie_worked():
    #     print(">>>> TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        # можно было просто написать request.POST
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
        if cat.author != request.user:
                raise Http404("You aren't the author of this category!")
    except Category.DoesNotExist:
                # cat = None
                return HttpResponse('This page does not exist! (You should pass existing url of category, but you pass '
                                     + '<strong>' + category_name_slug + '</strong>)')

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                # объект не будет сохранён в базу данных
                # будет только создан
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                # return HttpResponseRedirect(reverse('index', args=(cat.name,)))

                # я не заметил разницы,с тем что выше
                # так же проверено на кнопке назад
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})


@login_required
def change_category(request):
    errors = []
    if request.method == 'GET':
        information = request.GET['information']
        catid = request.GET['cat_id']

        if len(information) > 1000 or information == "":
            errors.append("Please make information with length less than 1000 characters and not empty.")
        cat = Category.objects.filter(id=catid)
        if cat.count() > 0 and len(errors)==0:
            cat = cat[0]
            if cat.author == request.user:
                information = escape(information)
                cat.information = information
                cat.save()
            else:
                errors.append("Who are you?")
        else:
            errors.append("This category doesn't exist")

        if len(errors) == 0:
            return HttpResponse("ok")

    else:
        errors.append("Please, use form.")

    return HttpResponse(errors[0])


@login_required
def change_page(request):
    errors = []
    if request.method == 'GET':
        information = request.GET['information']
        catid = request.GET['cat_id']
        page_id = request.GET['page_id']

        if len(information) > 200 or information == "":
            errors.append("Please make information with length less than 200 characters and not empty.")
        cat = Category.objects.filter(id=catid)
        page = Page.objects.filter(id=page_id, category=cat)
        if cat.count() > 0 and page.count() > 0 and len(errors) == 0:
            cat = cat[0]
            page = page[0]
            if cat.author == request.user:
                information = escape(information)
                page.information = information
                page.save()
            else:
                errors.append("Who are you?")
        else:
            errors.append("This page or category doesn't exist. Are you hacker?")

        if len(errors) == 0:
            return HttpResponse("ok")

    else:
        errors.append("Please, use form.")

    return HttpResponse(errors[0])


@login_required
def delete_page(request):
    if request.method == 'GET':
        page_id = request.GET['page_id']
        page = Page.objects.filter(id = page_id)[0]
        if page.category.author == request.user:
            page.delete()
        else:
            HttpResponse("You are not the owner!")
        return HttpResponse("ok")
    else:
        return HttpResponse("Please use the close button!")


@login_required
def add_category(request):
    errors = []
    if request.method == 'POST':
        name = request.POST['name']
        information = request.POST['information']

        if len(name) < 3 or len(name) > 20: errors.append("Please make name with length less than 128 and more than 2 characters.")
        if len(information) > 1000: errors.append("Please make information with length less than 1000 characters.")
        if Category.objects.filter(name=name).count() > 0:
            errors.append("This name already is used.")

        if len(errors) == 0:
            information = escape(information)
            cat = Category(name=name, author=request.user, information=information)
            count = Category.objects.filter(slug=slugify(name)).count()
            cat.save()
            if count > 0:
                cat.slug += "_" + str(count)
            cat.save()
            return category(request, cat.slug)
    else:
        # If the request was not a POST, display the form to enter details.
        errors.append("Please, use form.")

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'errors': errors})


@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        info = request.GET['information']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            if category.author != request.user:
                raise Http404("You aren't the author of this category!")
            # second parameter is boolean value which mean was or not madden new Page
            page, context_dict['created'] = Page.objects.get_or_create(category=category, title=title, url=url)
            page.information = escape(info)[:200]
            page.save()

            pages = Page.objects.filter(category=category).order_by('-views')

            # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages
            context_dict['category'] = category
            context_dict['category_name'] = category.name

    return render(request, 'rango/page_list.html', context_dict)


def category(request, category_name_slug, lock = False):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    context_dict['query'] = None
    context_dict['result_list'] = None

    if request.method == 'POST':
        query = request.POST.get('query', None)
        if query:
            # Run our Bing function to get the results list!
            if request.user.is_authenticated():
                context_dict['result_list'] = run_query(query)
            else:
                return redirect('auth_login')

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        if not category.open and not lock:
            if category.author != request.user:
                raise Http404("Category does not exist or you don't have access.")



        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category).order_by('-views')

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        context_dict['picture'] = UserProfile.objects.get(user=category.author).picture
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        raise Http404("Category does not exist!")
        # pass

    if not context_dict['query']:
        context_dict['query'] = category.name


    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)


def index(request):

    # request.session.set_test_cookie()

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.filter(open=True).order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    page_list = Page.objects.filter(category__open=True).order_by('-views')[:5]
    context_dict['pages'] = page_list

    visits = request.session.get('visits', 1)
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
        context_dict['time'] = last_visit
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True
        context_dict['time'] = datetime.now()

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits


    context_dict['visits'] = visits

    response = render(request,'rango/index.html', context_dict)

    return response


def index_about(request):
    context_dict = {'boldmessage': "about page!"}

    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.


    context_dict['visits'] = request.session.get('visits', 0)

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'rango/about.html', context_dict)


def index2(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "new page!"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context_dict)


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/rank/')


def some_view(request):
    if request.user.is_authenticated():
        return HttpResponse("You are logged in." + request.user.username)
    else:
        return HttpResponse("You are not logged in.")


def track_url(request):
    try:
        if request.method == 'GET':
            if 'page_id' in request.GET:
                page_id = request.GET['page_id']
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.last_visit = datetime.now()
                page.save()
                return redirect(page.url)
            else:
               # index is name of the view
               return redirect('index')
    except Page.DoesNotExist:
        return redirect('index')


@login_required
def register_profile(request):
    user = request.user
    registered = False

    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)

            try:
                prof = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                prof = None

            if prof:
                if profile.website != '':
                    prof.website = profile.website
                profile = prof
            else:
                profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            return redirect('index')

        else:
            print(profile_form.errors)

    else:
        if UserProfile.objects.filter(user=request.user).count() == 0:
            UserProfile(user=request.user).save()
        profile_form = UserProfileForm()

    return render(request, 'rango/profile_registration.html', {'profile_form': profile_form})


def profile(request, user_name):
    context = {}
    try:
        user = User.objects.get(username=user_name)
        context['current_user'] = user
        context['profile'] = UserProfile.objects.get(user=user)
        context['cats'] = Category.objects.filter(author=user).order_by('-open')
        return render(request, 'rango/profile.html', context)

    except :
        raise Http404("User does not exist!")
        # pass


@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)


def get_category_list(user=None, max_results=0, starts_with=''):

        cat_list = []

        if starts_with:
                cat_list = list(Category.objects.filter(name__istartswith=starts_with).filter(open=True)[:max_results])
                cat_list += list(Category.objects.filter(name__istartswith=starts_with).filter(open=False).filter(author=user))

        return cat_list[:max_results]


def suggest_category(request):
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']

        cat_list = get_category_list(request.user, 8, starts_with)

        return render(request, 'rango/category_list.html', {'cat_list': cat_list })


@login_required
def lock(request):
    user = request.user
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        try:
            # print(cat_id)
            cat = Category.objects.get(id=int(cat_id))
            if cat.author.id == user.id:
                cat.open ^= True
                print("Here")
                if not cat.open:
                    cat.lock = generate()
                cat.save()
            return render(request, 'inners/lock.html', {'cat': cat})
        except Category.DoesNotExist:
            pass
    return HttpResponse("Category does not exist")


def lockid(request, lockid):
    try:
        if lockid != "":
            cat = Category.objects.get(lock=lockid)
            return category(request, cat.slug, lock = True)
    except Category.DoesNotExist:
        pass
    return HttpResponse("Category key isn't valid!")

