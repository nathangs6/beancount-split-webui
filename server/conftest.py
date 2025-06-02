import os
import shutil

def pytest_configure(config):
    print("Configuring pytest...")
    os.environ["FAVA_DIR"] = os.path.abspath(os.path.dirname(__file__) + "/../test_data/fava")
    os.environ["USER_1_NAME"] = "Bob"
    os.environ["USER_2_NAME"] = "Joe"
    os.environ["USER_1_BEANCOUNT_FILE"] = "../test_data/fava/Bob/ledger.beancount"
    os.environ["USER_2_BEANCOUNT_FILE"] = "../test_data/fava/Joe/ledger.beancount"
    os.environ["SHARED_NAME"] = "Shared"
    os.environ["INDENT_STRING"] = "    "
    os.environ["CONFIG_FOLDER"] = os.path.abspath(os.path.dirname(__file__) + "/../test_data/config")
    shutil.copyfile("../test_data/fava/test_Bob.beancount", "../test_data/fava/Bob/ledger.beancount")
    shutil.copyfile("../test_data/fava/test_Joe.beancount", "../test_data/fava/Joe/ledger.beancount")
