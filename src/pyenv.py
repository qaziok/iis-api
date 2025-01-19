from dotenv import load_dotenv
import json
import os


def read_tests():
    with open('src/test.json') as f:
        tests = json.load(f)
    return tests


class Settings(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Tests(list):
    __getitem__ = list.__getitem__


load_dotenv()
settings = Settings({
    key.lower(): value for key, value in os.environ.items()
})
tests = Tests(read_tests())