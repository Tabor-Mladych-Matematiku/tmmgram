from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

with open("tmmgram.yaml", "r") as file:
    config = load(file, Loader)
