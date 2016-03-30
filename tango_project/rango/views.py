
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .bing_search import run_query


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
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
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
def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            # вернёт созданую модель после вызова

            # здесь объект будет и создан и сохранён в базу, последющих save не потребуется
            cat = form.save(commit=True)

            # print(cat.name, cat.slug)
            # Now call the index() view.
            # The user will be shown the homepage.
            # redirect("rango/")
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

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

        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        # raise Http404("Category does not exist!")
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)


def index(request):

    # request.session.set_test_cookie()

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    page_list = Page.objects.order_by('-views')[:5]
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
    return HttpResponseRedirect('/rango/')


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
        profile_form = UserProfileForm()


    return render(request, 'rango/profile_registration.html', {'profile_form': profile_form})


@login_required
def profile(request):
    context = {}
    try:
        context['profile'] = UserProfile.objects.get(user=request.user)

    except UserProfile.DoesNotExist:
        pass

    return render(request, 'rango/profile.html', context)