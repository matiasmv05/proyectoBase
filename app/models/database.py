from pymongo import MongoClient
import certifi
MONGO_URI = 'mongodb+srv://matiasmoron_db_user:RUsIJKMROh39u2ju@cluster0.euc0ue0.mongodb.net/dbb_products_app?retryWrites=true&w=majority&appName=Cluster0'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_products_app"]
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db
