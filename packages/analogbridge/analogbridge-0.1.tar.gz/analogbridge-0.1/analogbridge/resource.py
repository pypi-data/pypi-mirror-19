from analogbridge import *
import os


class Product():
    def __init__(self):
        pass

    @staticmethod
    def list():
        r = APIRequest(url="products", params=None, key_required=False)
        return r.call()


class Customer():
    def __init__(self):
        pass

    @staticmethod
    def find(customer_id):
        r = APIRequest(url="customers/" + customer_id)
        return r.call()

    @staticmethod
    def delete(customer_id):
        r = APIRequest(url="customers/" + customer_id, method="DELETE")
        return r.call()

    @staticmethod
    def create(params=None):
        r = APIRequest(url="customers", method="POST", params=params)
        return r.call()

    @staticmethod
    def update(customer_id, params=None):
        r = APIRequest(url="customers/" + customer_id, method="POST", params=params)
        return r.call()

    @staticmethod
    def list(limit=20, offset=0):
        params = {
            "limit": limit,
            "offset": offset
        }
        r = APIRequest(url="customers", params=params)
        return r.call()


class Order():
    def __init__(self):
        pass

    @staticmethod
    def where(customer_id=None, order_id=None):

        if order_id and customer_id:
            url = os.path.join("customers", customer_id, "orders", order_id)
        elif customer_id:
            url = os.path.join("customers", customer_id, "orders")
        else:
            raise Exception("customer id required")

        r = APIRequest(url=url)
        return r.call()

    @staticmethod
    def import_ready():
        r = APIRequest(url="orders/import-ready")
        return r.call()