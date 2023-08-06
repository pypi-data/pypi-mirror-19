from os.path import dirname, join

# This is BII-S-7 "Gut microflora Metagenomes in 2 different population fed a different diet"

try:
    import json as j
except ImportError as e:
    raise RuntimeError("BII-S-7 data requires json to be installed")

#  returns json representation of gutmicroflora.json
json = j.load(open(join(dirname(__file__), 'BII-S-7.json')))
