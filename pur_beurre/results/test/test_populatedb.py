#!/usr/bin/python3
# coding : utf-8

import os
import json
import pytest

from results.models import Pb_Products
from results.management.commands.populatedb import Command


def j(json_file):
    """This function opens and returns a json file
    in test/samples/
    :param json_file: str, 'valid_off.json'
    :return: dict, the file
    """
    path = os.path.join("results/test/samples/", json_file)
    with open(path, "r") as file_a:
        json_file = file_a.read()
    return json.loads(json_file)


@pytest.mark.skip()
@pytest.mark.django_db
class TestPopulateDB():

    def test_valid(self, patch_get_and_load):
        popdb = Command()
        patch_get_and_load.values = j("populatedb_valid.json")
        popdb.handle()
        prods = Pb_Products.objects.all()
        assert len(prods) == 2

    def test_invalid(self, patch_get_and_load):
        popdb = Command()
        patch_get_and_load.values = j("populatedb_invalid.json")
        popdb.handle()
        prods = Pb_Products.objects.all()
        assert len(prods) == 1
