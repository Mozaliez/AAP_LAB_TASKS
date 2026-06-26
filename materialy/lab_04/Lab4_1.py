# -*- coding: utf-8 -*-
"""Zadanie 1 -- Random User API to SQL (SQLite)."""

import sqlite3
import requests

# 1. Pobierz dane z API
response = requests.get("https://randomuser.me/api/?results=30")
users = response.json()["results"]

# Połączenie z bazą danych w pamięci RAM (wygodne do testów) lub do pliku np. "users.db"
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# 2. Stworz tabele Users (id, first_name, last_name, email, age, gender, country)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    age INTEGER,
    gender TEXT,
    country TEXT
)
""")
conn.commit()

# 3. Wstaw dane z parametryzacja (? nie f-string!)
insert_query = """
INSERT INTO Users (first_name, last_name, email, age, gender, country)
VALUES (?, ?, ?, ?, ?, ?)
"""

for user in users:
    # Wyciągamy odpowiednie pola ze struktury JSON dostarczonej przez API
    first_name = user["name"]["first"]
    last_name = user["name"]["last"]
    email = user["email"]
    age = user["dob"]["age"]
    gender = user["gender"]
    country = user["location"]["country"]
    
    # Bezpieczne wykonanie zapytania z krotką parametrów
    cursor.execute(insert_query, (first_name, last_name, email, age, gender, country))

conn.commit()

# 4. Zapytania analityczne
print("--- ANALIZA DANYCH SQL ---\n")

# A. Ile jest mężczyzn, a ile kobiet?
print("Liczba osób według płci:")
cursor.execute("SELECT gender, COUNT(*) FROM Users GROUP BY gender")
for gender, count in cursor.fetchall():
    print(f"  * {gender}: {count}")

print("-" * 30)

# B. Jaki jest średni wiek?
cursor.execute("SELECT AVG(age) FROM Users")
avg_age = cursor.fetchone()[0]
print(f"Średni wiek użytkowników: {avg_age:.1f} lat")

print("-" * 30)

# C. W ilu krajach mieszkają? (oraz zestawienie)
cursor.execute("SELECT COUNT(DISTINCT country) FROM Users")
distinct_countries = cursor.fetchone()[0]
print(f"Użytkownicy mieszkają w {distinct_countries} różnych krajach.")

print("\nSzczegółowe zestawienie krajów:")
cursor.execute("SELECT country, COUNT(*) FROM Users GROUP BY country ORDER BY COUNT(*) DESC")
for country, count in cursor.fetchall():
    print(f"  * {country}: {count}")

# Zamknięcie połączenia z bazą danych
conn.close()