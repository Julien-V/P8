from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import json

from datetime import datetime as dt

from results.models import Pb_Categories_Products as pb_cat_prod
from results.models import Pb_Products
from results.models import Pb_Favorite

from results.forms import ConnectionForm, RegisterForm


def index(req):
    return render(req, "index.html")


# Create your views here.
def search_results(req):
    query = req.GET.get('query')
    if not query:
        prod = Pb_Products.objects.all()
    else:
        prod = Pb_Products.objects.filter(
            product_name__icontains=query)
    if not prod.exists():
        prod = Pb_Products.objects.all()
    nG = 'nutrition_grades'
    # get cat of first elem in prod
    choosen_nG = prod[0].nutrition_grades
    cat = pb_cat_prod.objects.filter(product=prod[0])[0].category
    # get substitutes for choosen cat
    elem_list = pb_cat_prod.objects.filter(category=cat)
    prod_list = [x.product for x in elem_list]
    # get substitutes with better nutrition_grades than product's
    subs_list = [x for x in prod_list if x.nutrition_grades < choosen_nG]
    # sort them
    sorted_subs_list = sorted(
        subs_list,
        key=lambda i: i.nutrition_grades
    )
    context = {
        'product_searched': prod[0],
        'products': sorted_subs_list
    }
    return render(req, "results.html", context)


@login_required
def substitute(req):
    if req.method == "POST":
        query = req.POST.get('code')
        if not query:
            return redirect('./home')
        else:
            prod = Pb_Products.objects.filter(
                code__contains=int(query))
        if not prod.exists():
            return redirect('./home')
        user = User.objects.filter(username__contains=req.user)[0]
        fav = Pb_Favorite(
            user_id=user,
            product_id=prod[0],
            updated_timestamp=int(dt.now().timestamp()))
        fav.save()
        return redirect('./home')
    else:
        user = User.objects.filter(
            username__contains=req.user)[0]
        subs = Pb_Favorite.objects.filter(user_id=user)
        context = {
            "subs": [x.product_id for x in subs]
        }
        return render(req, "substitute.html", context)


def user_auth(req):
    error = False
    if req.method == "POST":
        form = ConnectionForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Vérification
            user = authenticate(
                username=username,
                password=password)
            if user:
                login(req, user)
            else:
                error = True
    else:
        form = ConnectionForm()
    return render(req, 'authentification.html', locals())


@login_required
def user_deauth(req):
    logout(req)
    return redirect("./home")


def user_reg(req):
    error = False
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            temp = req.POST.copy()
            temp["username"] = temp["email"]
            form = RegisterForm(temp)
            if form.is_valid():
                form.save()
                return redirect("/home")
    else:
        form = RegisterForm()
    return render(req, 'register.html', locals())


def terms(req):
    return render(req, 'terms.html')


def product(req):
    query = req.GET.get('code')
    if not query:
        prod = Pb_Products.objects.all()
    else:
        prod = Pb_Products.objects.filter(
            code__contains=query)[0]
    if not prod:
        pass
        # return 404
    else:
        req100 = json.loads(prod.req100.replace('-', ''))
        ng = prod.nutrition_grades.upper()
        ng_image = f"/static/assets/img/Nutri-{ng}.png"
        context = {
            'ng_image': ng_image,
            'product_searched': prod,
            'req100': req100
        }
    return render(req, 'product.html', context)


@login_required
def account(req):
    return render(req, 'account.html', locals())
