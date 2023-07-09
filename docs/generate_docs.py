from flask import Blueprint
from inspect import (
    getmembers,
    isfunction,
    getsource,
)
import json
import re
from typing import Any
import yaml

from pydantic.json_schema import models_json_schema

import grau.blueprints.user.routes as routes
from grau.db.user.user_model import UserSchema

MODULES = [routes]
VALIDATION_SCHEMAS = [UserSchema]


def get_url_methods(func: callable) -> tuple[Any]:
    """Get url and methods from route function docstrings

    Args:
        func (callable): blueprint route function

    Returns:
        _type_: url, methods
    """

    string = getsource(func).split("\n")[0]
    res = re.findall(r"\((.*?)\)", string.split("\n")[0])[0].split(",")

    return (
        res[0].replace('"', "").replace("'", "").strip(),  # url
        eval(res[1].split("=")[1].strip())
        if len(res) == 2
        else ["GET"],  # methods
    )


if __name__ == "__main__":
    paths = {}
    for module in MODULES:
        # Getting the blueprint name
        # Used to filter out functions that are not part of the blueprint
        blueprint = [
            name
            for name, func in vars(module).items()
            if isinstance(func, Blueprint)
        ]
        blueprint = blueprint[0] if blueprint else None
        if blueprint is None:
            continue
        else:
            blueprint = f"@{blueprint}.route"
            # getmembers returns a list of tuples (name, function)
            # it'll return function defs and callables
            functions = getmembers(routes, isfunction)
            for tup in functions:
                if blueprint not in getsource(tup[1]):
                    continue
                name, func = tup
                # get url and methods from docstring
                # We don't care about the methods here
                # Will include the methods in function docstrings
                url, _ = get_url_methods(func)
                try:
                    # load yaml docstring
                    docstring = yaml.safe_load(func.__doc__)
                except:
                    docstring = None
                # add url and docstring to paths
                paths[url] = docstring

    # Generate json schema for validation schemas
    _, validation_schema_json = models_json_schema(
        [(model, "validation") for model in VALIDATION_SCHEMAS],
        ref_template="#/components/schemas/{model}",
    )

    # Generate swagger.json
    swagger_dict = {
        "openapi": "3.0.0",
        "info": {
            "title": "GRAU API",
            "description": "The GRAU API: a RESTful API for the GRAU project. Bringing the power to the people.",
            "version": "1.0.0",
        },
        # Servers are used for the Swagger UI to make requests
        "servers": [
            {"url": "http://localhost:5000", "description": "Local server"}
        ],
        # Paths are the routes
        "paths": paths,
        # Components are the schemas
        "components": {
            "schemas": validation_schema_json["$defs"],
        },
    }

    with open("swagger.json", "w") as f:
        json.dump(swagger_dict, f, indent=4)
