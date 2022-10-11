import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from Constants import FIREBASE_DB_URL, FIREBASE_SDK_KEY

cred_obj = firebase_admin.credentials.Certificate(FIREBASE_SDK_KEY)
default_app = firebase_admin.initialize_app(cred_obj,
                                            {'databaseURL': FIREBASE_DB_URL})

ref = db.reference("/")
signedup_ref = db.reference("/signedup/")
waitlist_ref = db.reference("/waitlisted/")


def reset_db():
    ref.delete()


def get_lists():
    signedup = get_list(signedup_ref)
    waitlist = get_list(waitlist_ref)
    print(signedup, waitlist)
    return signedup, waitlist


def add_to_db(value, ref_type):
    ref_type.push().set(value)


def delete_from_db(value, ref):
    # ref = db.reference(type)
    dct = ref.get()
    if dct == None:
        return False

    print(dct)
    for key in dct:
        if dct[key] == value:
            dct.pop(key)
            ref.set(dct)
            return True
    return False


def get_list(ref):
    lst = ref.get()
    if lst:
        return lst
    return {}