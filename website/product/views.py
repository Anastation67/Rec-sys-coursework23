from django.shortcuts import redirect, render
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .forms import AddForm
from .models import Supplier




def home_view(request):
    error = None
    no_discounted = 0
    no_rised = 0
    form = AddForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
        except AttributeError:
            error = "Impossible to get the name or the price - the good might have been sold out"
        except:
            error = "Something went completely wrong :("

    form = AddForm()

    qs = Supplier.objects.all()
    items_no = qs.count()


    context = {
        'qs': qs,
        'items_no': items_no,
        'no_discounted': no_discounted,
        'no_rised': no_rised,
        'form': form,
        'error': error,
    }
    
    return render(request, 'product/main.html', context)
