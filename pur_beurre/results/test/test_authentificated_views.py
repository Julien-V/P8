#!/usr/bin/python3
# coding : utf-8

import pytest

from bs4 import BeautifulSoup

from django.urls import reverse

from results.models import Pb_Favorite


@pytest.mark.django_db
def test_add_subs(login_user):
    context = {"code": 3023290008393}
    client = login_user()
    url = reverse('substitute')
    response = client.post(url, context)
    # we should be redirected to "/"
    assert response.status_code == 302
    assert response.url == reverse('home')
    # product code should be in Pb_Favorite
    user = client.session['_auth_user_id']
    subs = Pb_Favorite.objects.filter(user_id=user)
    prods_code = [x.product_id.code for x in subs]
    assert context['code'] in prods_code


@pytest.mark.django_db
def test_get_subs(subs_added):
    client = subs_added()
    url = reverse('substitute')
    response = client.get(url)
    assert response.status_code == 200
    page = BeautifulSoup(response.content, features="html.parser")
    product_col = page.find("div", {'id': 'product-col'})
    assert product_col.find("p").contents[0] == "Sveltesse choco noir"


@pytest.mark.django_db
def test_logout_view(login_user):
    client = login_user()
    url = reverse('deauthentification')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')