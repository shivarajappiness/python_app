from django.shortcuts import render
from django.http import HttpResponse
from books.models import Book
from books.forms import ContactForm
from forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail



def search_form(request):
	form_ = ContactForm
	contacts = {"forms1":form_}
	return render(request, 'search_form.html', contacts)

# def search(request):
#     if 'q' in request.GET:	
#         message = 'You searched for: %r' % request.GET['q']
#     else:
#         message = 'You submitted an empty form.'
#     return HttpResponse(message)
def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'search_results.html',
                          {'books': books, 'query': q})
    return render(request, 'search_form.html',
                  {'errors': errors})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'shivaraj.appiness@gmail.com'),
                ['shivaraj.appiness@gmail.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form':form})