from django.shortcuts import render
from django.http import HttpResponse

from .forms import OptForm, CircleAreaForm, RectanglePerimeterForm

from .calcs import _circle_area, _rectangle_perimeter

# Create your views here.
def start(request):
    opt_form = OptForm()
    return render(request, 'mathcalc/index.html', {'opt_form' : opt_form})

def select_choice(request):
    opt = request.POST['shape_choice']
    if opt == 'circle':
        cArea_form = CircleAreaForm()
        return render(request, 'mathcalc/area_circle.html', {'cArea_form' : cArea_form})
    elif opt == 'rect':
        rPerimeter_form = RectanglePerimeterForm()
        return render(request, 'mathcalc/perimeter_rectangle.html',
                      {'rPerimeter_form' : rPerimeter_form})

def area_circle(request):
    radius = int(request.POST['radius_value'])
    area_value = _circle_area(radius)
    circle_vals = {
        'radius' : radius,
        'area_value' : area_value
    }
    return render(request, 'mathcalc/circle_result.html', {'circle_vals' : circle_vals })

def perimeter_rectangle(request):
    length = int(request.POST['length_value'])
    breadth = int(request.POST['breadth_value'])
    perimeter = _rectangle_perimeter(length, breadth)
    rectangle_vals = {
        'length' : length,
        'breadth' : breadth,
        'perimeter' : perimeter
    }
    return render(request, 'mathcalc/rectangle_result.html', {'rectangle_vals' : rectangle_vals})

