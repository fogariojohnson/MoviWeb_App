import json

users = {
    1: {
        "name": "Alice",
        "movies": {
            1: {
                "title": "Inception",
                "director": "Christopher Nolan",
                "year": 2010,
                "rating": 8.8
            },
            2: {
                "title": "The Dark Knight",
                "director": "Christopher Nolan",
                "year": 2008,
                "rating": 9.0
            }
        }
    },
    2: {
        "name": "Bob",
        "movies": {
            1: {
                "title": "John Wick: Chapter 4",
                "director": "Chad Stahelski",
                "year": 2023,
                "rating": 7.9
            },
            2: {
                "title": "Avengers: Endgame",
                "director": "Anthony and Joe Russo",
                "year": 2019,
                "rating": 8.4
            }
        }
    }
}

# Convert the dictionary to JSON format
json_data = json.dumps(users, indent=4)

# Save the JSON data to a file
with open("storage/user.json", "w") as file:
    file.write(json_data)
