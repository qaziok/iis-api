from dotenv import load_dotenv
import os


class Settings(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


load_dotenv()
settings = Settings({
    key.lower(): value for key, value in os.environ.items()
})

print(settings.path)
