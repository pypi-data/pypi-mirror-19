import random, time, os, sys

__version__ = "1.0.2"

def makeTemplate(templatepath, **variables):
    newtemplatepath = templatepath

    with open(newtemplatepath, "r") as templatefile:
        template = templatefile.read()

    for key, value in variables.items():
        template = template.replace("{{%s}}" % key, value)

    return template.replace("\{", "{").replace("\}", "}")

def getHeaderDict(fieldstorage):
    return dict([
        (name, val.value) for name, val in dict(fieldstorage).iteritems()
    ])
