from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

import requests
import json
import datetime

from pur_beurre.settings import off_api
from results.models import Categorie as db_cat
from results.models import Product as db_prod
from results.models import CategoriesProducts as db_cat_prod


class Command(BaseCommand):
    help = 'Fill DB with OpenFoodFacts data'

    def __init__(self, args=off_api):
        self.url = args['url']
        self.headers = args['headers']
        self.params = args['params']
        self.categories = args['categories']
        self.fields = args['fields']
        self.req100 = args['req100']
        self.count = 0

    def keep_nutri_g_only(self):
        """This method keeps only products with nutrition grades"""
        prod_list = self.result_list
        temp = [x for x in prod_list if 'nutrition_grades' in x.keys()]
        self.result_list = temp

    def get_and_load(self, params):
        """This method does the request and decode returned JSON
        :return: JSON decoded by json.loads()
        """
        requesting = True
        nb_try = 0
        while requesting and nb_try < 4:
            try:
                r = requests.get(
                    self.url,
                    headers=self.headers,
                    params=params)
                requesting = False
            except requests.exceptions.Timeout:
                self.stdout.write('[!] populatedb : Timeout')
            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    f'[!] populatedb : error {e}')
            nb_try += 1
        if not requesting:
            result = json.loads(r.text)
        else:
            result = None
        return result

    def insert_in_db(self, cat):
        for product in self.result_list:
            prod_dict = dict()
            for key in product.keys():
                if key in self.fields:
                    prod_dict[key] = product[key]
            # code should be int not str
            if 'code' in prod_dict.keys():
                if isinstance(prod_dict["code"], str):
                    prod_dict["code"] = int(prod_dict["code"])
            # Get req100 from 'nutriments'
            if 'nutriments' in prod_dict.keys():
                req100_temp = dict()
                for key in self.req100:
                    if key in prod_dict['nutriments']:
                        req100_temp[key] = prod_dict['nutriments'][key]
                req100 = json.dumps(req100_temp)
                prod_dict['req100'] = req100
                prod_dict.pop('nutriments', None)
            # add creation timestamp
            ts = datetime.datetime.now().timestamp()
            prod_dict['added_timestamp'] = int(ts)
            # insert into Product
            prod_db = db_prod(**prod_dict)
            try:
                prod_db.clean()
                prod_db.save()
                cat_prod = db_cat_prod(
                    category_id=cat.id,
                    product_id=prod_db.id
                )
                cat_prod.save()
            except ValidationError as e:
                print(e)

    def run(self, cat):
        # add cat db
        cat_db = db_cat(category_name=cat)
        cat_db.save()
        # get products in cat from OFF API
        self.result_list = list()
        params = self.params.copy()
        params['tag_0'] = cat
        result = self.get_and_load(params)
        if "count" in result.keys():
            self.count = int(result['count'])
            if 'products' in result.keys():
                self.result_list += result['products']
                while self.count > len(self.result_list):
                    params['page'] = int(params['page'])+1
                    result = self.get_and_load(params)
                    if 'products' in result.keys():
                        self.result_list += result['products']
                    else:
                        break
        self.keep_nutri_g_only()
        self.insert_in_db(cat_db)

    def handle(self, *args, **options):
        for cat in self.categories:
            if db_cat.objects.filter(category_name=cat).exists():
                print(f"[*] '{cat}'' already populated")
            else:
                print(f"[*] '{cat}' empty, running populatedb.run('{cat}')")
                self.run(cat)
