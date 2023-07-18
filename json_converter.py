import json

users = {
    1: {
        "name": "Alice",
        "movies": {
            1: {
                "title": "Inception",
                "director": "Christopher Nolan",
                "year": 2010,
                "rating": 8.8,
                "poster": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg",
                "genre": "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F47D.png",
                "flag": "https://flagsapi.com/US/shiny/64.png",
                "url": "https://www.imdb.com/title/tt1375666/?ref_=nv_sr_srsg_0_tt_8_nm_0_q_Incep"
            },
            2: {
                "title": "The Dark Knight",
                "director": "Christopher Nolan",
                "year": 2008,
                "rating": 9.0,
                "poster": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg",
                "genre": "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F4A3.png",
                "flag": "https://flagsapi.com/US/shiny/64.png",
                "url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg"
            }
        }
    },
    2: {
        "name": "Bob",
        "movies": {
            1: {
                "title": "Star Wars: Episode V",
                "director": "Irvin Kershner",
                "year": 1980,
                "rating": 8.7,
                "poster": "https://m.media-amazon.com/images/M/MV5BYmU1NDRjNDgtMzhiMi00NjZmLTg5NGItZDNiZjU5NTU4OTE0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
                "genre": "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F4A3.png",
                "flag": "https://flagsapi.com/US/shiny/64.png",
                "url": "https://www.imdb.com/title/tt0080684/?ref_=nv_sr_srsg_4_tt_7_nm_0_q_Star%2520Wars%253A%2520Episode%2520V"
            },
            2: {
                "title": "Titanic",
                "director": "James Cameron",
                "year": 1997,
                "rating": 7.9,
                "poster": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg",
                "genre": "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F62D.png",
                "flag": "https://flagsapi.com/US/shiny/64.png",
                "url": "https://www.imdb.com/title/tt0120338/"
            }
        }
    }
}

# Convert the dictionary to JSON format
json_data = json.dumps(users, indent=4)

# Save the JSON data to a file
with open("storage/user.json", "w") as file:
    file.write(json_data)
