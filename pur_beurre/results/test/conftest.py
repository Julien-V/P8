#!/usr/bin/python3
# coding : utf-8


import pytest

from django.contrib.auth.models import User

from django.core.management import call_command
from results.management.commands.populatedb import Command

from django.urls import reverse

from results.models import Pb_Favorite


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'results_data.json')


@pytest.fixture
def reg_user():
    def make_reg():
        User.objects.create_user(
                username="usertest",
                password="test1password"
            )
    return make_reg


@pytest.fixture
def login_user(client, reg_user):
    def make_login():
        reg_user()
        client.login(
            username='usertest',
            password='test1password'
        )
        return client
    return make_login


@pytest.fixture
def subs_added(login_user):
    def make_subs():
        context = {"code": 3023290008393}
        client = login_user()
        url = reverse('substitute')
        response = client.post(url, context)
        # product code should be in Pb_Favorite
        user = client.session['_auth_user_id']
        subs = Pb_Favorite.objects.filter(user_id=user)
        prods_code = [x.product_id.code for x in subs]
        assert context['code'] in prods_code
        return client
    return make_subs


@pytest.fixture
def patch_get_and_load(monkeypatch):
    """This function monkeypatchs Command.get_and_load
    with mock_get_and_load. Create a FakeJSON_file class which is
    used to get a json file
    """
    def mock_get_and_load(*args):
        """This function return var values from class FakeJSON_file
        :return: json file in a dict (json.loads())
        """
        return json_file.values
    monkeypatch.setattr(Command, "get_and_load", mock_get_and_load)

    class FakeJSON_file:
        pass

    json_file = FakeJSON_file()
    json_file.values = None
    return json_file