import os
FAVA_DIR = os.environ.get("FAVA_DIR", os.path.abspath(os.path.dirname(__file__) + "/../../test_data/fava"))
_user_1_name = os.environ.get("USER_1_NAME", "Bob")
USER_1 = {
    "name": _user_1_name,
    "beancount_file": os.path.abspath(FAVA_DIR + "/" + _user_1_name + "/ledger.beancount"),
    "beancount_folder": os.path.abspath(FAVA_DIR + "/" + _user_1_name)
}
_user_2_name = os.environ.get("USER_2_NAME", "Bob")
USER_2 = {
    "name": _user_2_name,
    "beancount_file": os.path.abspath(FAVA_DIR + "/" + _user_2_name + "/ledger.beancount"),
    "beancount_folder": os.path.abspath(FAVA_DIR + "/" + _user_2_name)
}
USERS = {
    USER_1["name"]: USER_1,
    USER_2["name"]: USER_2
}
USERS_LIST = [USER_1, USER_2]
SHARED_NAME = os.environ.get("SHARED_NAME", "Shared")
INDENT_STRING = os.environ.get("INDENT_STRING", "    ")
