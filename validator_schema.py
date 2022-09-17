book_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "author", "publish_date", "type", "copies"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "author":{
                "bsonType":"array",
                "items":{
                    "bsonType": "objectId",
                    "description": "must be a objectId and is required"
                }

            },
            "publish_date":{
                "bsonType": "date",
                "description": "must be a date and is required"
            },
            "type": {
                "enum": ["Ficcion", "Non-Ficcion"],
                "description": "can only be one of the enum values and is required"
            },
            "copies":{
                "bsonType": "int",
                "minimum": 0,
                "description": "must be a interger greater than 0 and is required"
            }
        }
    }
}

author_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["first_name", "last_name", "date_of_bird"],
        "properties": {
            "first_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "last_name":{
                "bsonType":"string",
                "description": "must be a string and is required"
            },
            "date_of_bird":{
                "bsonType": "date",
                "description": "must be a date and is required"
            },
        }
    }
}