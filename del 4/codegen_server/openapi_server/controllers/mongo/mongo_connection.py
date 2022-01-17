import pymongo

# connect to cluster on cloud
client = pymongo.MongoClient("mongodb+srv://user1:user1_password@watchlistapp.ubtwk.mongodb.net"
                                "/myFirstDatabase?retryWrites=true&w=majority")

# connect to database on cluster
db = client.watchlist_app


