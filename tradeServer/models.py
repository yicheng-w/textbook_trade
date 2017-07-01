from mongoengine import *
import time
import datetime
from functools import wraps

from . import settings
from . import utils

# exceptions
class NotInCartException(Exception):
    pass
class NoSuchItemException(Exception):
    pass

class User(Document):
    u_id = StringField(required=True, primary_key=True)
# inventory: {item_id : }
    sell_inventory = DictField()
    buy_inventory = DictField()
    name = StringField(required=True)
    api_key = StringField(required=True)
    admin = BooleanField()

    def init(self, name, u_id):
        self.u_id = u_id
        self.name = name
        self.buy_inventory = {}
        self.sell_inventory = {}
        self.api_key = utils.gen_new_api_key()
        self.admin = False
        self.save()

    def add_item_to_cart(self, item, quality=1):
        """
        add the item to buy_inventory, add buyer to watch list
        """
        if item.available:
            if str(item.id) in self.buy_inventory:
                self.buy_inventory[str(item.id)] += 1
            else:
                self.buy_inventory[str(item.id)] = 1

            item.added_to_cart(self)

        raise NoSuchItemException

    def remove_item_from_cart(self, item, quality=1):
        """
        remove item from sell_inventory, remove buyer from watch list
        """
        if str(item.id) in self.buy_inventory:
            if self.buy_inventory[str(item.id)] >= 1:
                self.buy_inventory[str(item.id)] -= 1

            if self.buy_inventory[str(item.id)] == 0:
                item.removed_from_cart(self)

            raise NotInCartException
        raise NotInCartException

