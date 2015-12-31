from .definitions import Definitions
from .paths import Paths

EXAMPLE_SWAGGER_JSON = {
    "info": {"title": "myApi", "version": "1.0"},
    "swagger": "2.0",
    "tags": [{
        "name": "pet"
    }],
    "paths": {
        "/deck/add_card": {
            "post": {
                "tags": ["card"],
                "summary": "add a card to a deck.",
                "description": "",
                "produces": ["application/json"],
                "parameters": [{
                    "in": "body",
                    "name": "body",
                    "required": True,
                    #"schema": {
                    #   "$ref": "#/definitions/Card"
                    #}
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                }],
                "responses": {
                    "200": {"description": "good input"}
                }
            }
        }
    },
    "definitions": {
        "Card": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"}
            }
        }
    }
}
