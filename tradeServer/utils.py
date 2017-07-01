import string
import random

from . import settings

def gen_new_api_key():
    keyset = string.ascii_letters + string.digits
    return "".join([random.choice(keyset) for _ in range(settings.API_KEY_LENGTH)])
