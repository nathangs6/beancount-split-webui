import os
import shutil

def pytest_configure(config):
    print("Configuring pytest...")
    os.environ["FAVA_DIR"] = os.path.abspath(os.path.dirname(__file__) + "/../fava")
    os.environ["USER_1_NAME"] = "Bob"
    os.environ["USER_2_NAME"] = "Joe"
    os.environ["USER_1_BEANCOUNT_FILE"] = "../fava/Bob/ledger.beancount"
    os.environ["USER_2_BEANCOUNT_FILE"] = "../fava/Joe/ledger.beancount"
    os.environ["SHARED_NAME"] = "Shared"
    os.environ["INDENT_STRING"] = "    "
    shutil.copyfile("../fava/test_Bob.beancount", "../fava/Bob/ledger.beancount")
    shutil.copyfile("../fava/test_Joe.beancount", "../fava/Joe/ledger.beancount")
