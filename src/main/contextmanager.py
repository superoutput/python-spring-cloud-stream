import json
import contextvars

def load(filepath):
    print(f"Hello {name.get()}")
    with open(filepath, "r") as read_file:
    data = json.load(read_file)
    for key, value in flattenJson(data).items():
        print("Key: %s Value: %s" % (key,value))
        contextvars.ContextVar(key).set(value)

def flattenJson(data, result=None):
    if result is None:
        result = {}
    for key in data:
        value = data[key]
        if isinstance(value, dict):
            subvalue = {}
            for subkey in value:
                subvalue[".".join([key,subkey])]=value[subkey]
            flattenJson(subvalue, result)
        elif isinstance(value, (list, tuple)):   
            for indexB, element in enumerate(value):
                if isinstance(element, dict):
                    subvalue = {}
                    index = 0
                    for subkey in element:
                        #newkey = ".".join([key,subkey])        
                        subvalue[".".join([key,subkey])]=value[indexB][subkey]
                        index += 1
                    for keyA in subvalue:
                        flattenJson(subvalue, result)   
        else:
            result[key]=value
    return result

def listContext():
    ctx = contextvars.copy_context()
    return list(ctx.items())

def get(key):
    return contextvars.ContextVar(key).get()

def add(key, value):
    contextvars.ContextVar(key).set(value)

def remove(key):
    contextvars.ContextVar(key).reset()