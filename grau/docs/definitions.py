from pydantic.json_schema import models_json_schema
import json

from grau.db.user.user_model import UserValidationSchema


def generate_schema_defintions() -> dict:
    """ """
    validation_models = [UserValidationSchema]
    return UserValidationSchema.model_json_schema()


if __name__ == "__main__":
    schema_json = generate_schema_defintions()

    with open("defintions.yaml", "w") as f:
        f.write(json.dumps(schema_json, indent=2))
