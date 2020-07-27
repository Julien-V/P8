from django.shortcuts import render

from results.models import Pb_Categories_Products, Pb_Categories, Pb_Products


# Create your views here.
def search_results(req):
    return render(req, "results.html")


def substitute(req):
    return render(req, "substitute.html")