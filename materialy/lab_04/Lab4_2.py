"""Zadanie 2 -- GeckoTerminal API to MongoDB."""

from pymongo import MongoClient
import requests

# Nawiązujemy połączenie z lokalną bazą MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.lab4
networks_collection = db["networks"]

# Czyścimy kolekcję przed ponownym uruchomieniem (opcjonalnie, zapobiega duplikatom)
networks_collection.drop()

# Pobieramy dane o sieciach kryptowalutowych z API
response = requests.get("https://api.geckoterminal.com/api/v2/networks")
data = response.json()["data"]

# Wstawiamy pobrane dokumenty bezpośrednio do kolekcji
networks_collection.insert_many(data)

# Tworzymy potok agregacji grupujący sieci po ich typie
pipeline = [
    {
        "$group": {
            "_id": "$attributes.type", 
            "count": {"$sum": 1}
        }
    },
    {
        "$sort": {"count": -1}
    }
]

# Wyświetlamy podsumowanie agregacji w terminalu
print("--- LICZBA SIECI PER TYP ---")
for doc in networks_collection.aggregate(pipeline):
    # Obsługujemy sytuację, gdyby typ był zapisany bezpośrednio w głównym polu 'type'
    if doc["_id"] is None:
        # Alternatywna próba pogrupowania po głównym polu 'type'
        pipeline_fallback = [
            {"$group": {"_id": "$type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        for fallback_doc in networks_collection.aggregate(pipeline_fallback):
            print(f"Typ: {fallback_doc['_id']} -> Ilość: {fallback_doc['count']}")
        break
    
    print(f"Typ: {doc['_id']} -> Ilość: {doc['count']}")

# Zamykamy połączenie z bazą danych
client.close()