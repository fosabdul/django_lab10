
from django.shortcuts import render, redirect, get_object_or_404

from .models import Place
from .forms import NewPlaceForm, TripReviewForm 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
# from django.conf.urls import url

@login_required

def place_list(request):

    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) # Create a new Place from the form # this is the where the error is coming from 
                                         # get the data but don't save it yet
        place.user = request.user  # save and redirect
        if form.is_valid(): 
            # place.visited = True    # Checks against DB constraints, for example, are required fields present? 
            place.save()        # Saves to the database 
            return redirect('place_list')    # redirects to GET view with name place_list - which is this same view 


    # If not a POST, or the form is not valid, render the page 
    # filter(user=request.user) = this will filter the places belong to the currently loggin in user
    #than filter that is not yet visited
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form })

@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True).order_by('name')
    form = NewPlaceForm()
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })
    # this return the template and data from the database

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':

        place = get_object_or_404(Place, pk=place_pk)  # 404 = if not found it will return 404
        if place.user == request.user:
            place.visited = True
            place.save()

        else:
            place.visited = True
            place.save()
            return HttpResponseForbidden()
       
    
    return redirect('place_list')  # redirect to wishlist places


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user != request.user:
        return HttpResponseForbidden


    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
           form.save()
           messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk) 
     # if the place details belong the user that is choosing the changes
    # if GET reqeust show the place if not = Post validaete form data and update
    #request.POST, = if you write a post
    # request.FILES, = if you update a file
    # 

    else:
        #if Get = show the place if not show the form

        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form} )

        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete() # after the place is deleted the browser will not show any thing you have to create redirect 
        return redirect('place_list')

    else:

         return HttpResponseForbidden

