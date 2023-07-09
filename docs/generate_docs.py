import json
import re
from ast import literal_eval
from inspect import getmembers, getsource, isfunction
from typing import Callable

import yaml
from flask import Blueprint
from pydantic.json_schema import models_json_schema

from grau.blueprints.user import routes
from grau.db.user.user_model import UserSchema

MODULES = [routes]
VALIDATION_SCHEMAS = [UserSchema]


def get_url_methods(route_function: Callable) -> tuple[str, list[str]]:
    """Get url and methods from route function docstrings

    Args:
        route_function (Callable): blueprint route function

    Returns:
        _type_: url, methods
    """

    string = getsource(route_function).split("\n", 1)[0]
    res = re.findall(r"\((.*?)\)", string.split("\n")[0])[0].split(",")

    return (
        res[0].replace('"', "").replace("'", "").strip(),  # url
        literal_eval(res[1].split("=")[1].strip())
        if len(res) == 2
        else ["GET"],  # methods
    )


if __name__ == "__main__":
    paths = {}
    for module in MODULES:
        # Getting the blueprint name
        # Used to filter out functions that are not part of the blueprint
        blueprint = None
        for name, func in vars(module).items():
            if isinstance(func, Blueprint):
                blueprint = name
                break
        if blueprint is None:
            continue
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
            url, methods = get_url_methods(func)
            try:
                # load yaml docstring
                docstring = yaml.safe_load(func.__doc__)
            except AttributeError as e:
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
            "description": (
                "The GRAU API: a RESTful API for the GRAU project."
                "Bringing the power to the people."
            ),
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
            "securitySchemes": {
                "cookieAuth": {
                    "type": "apiKey",
                    "in": "cookie",
                    "name": "session",
                }
            },
            "schemas": validation_schema_json["$defs"],
        },
    }

    with open("swagger.json", "w", encoding="utf-8") as f:
        json.dump(swagger_dict, f, indent=4)
