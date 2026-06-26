"""Zadanie 3 BONUS -- symulacja wyszukiwania wektorowego."""

import numpy as np

# Baza danych filmów z gotowymi embeddingami trójwymiarowymi
filmy = {
    "Incepcja":          np.array([0.8, 0.3, 0.9]),
    "Matrix":            np.array([0.75, 0.35, 0.85]),
    "Toy Story":         np.array([0.2, 0.9, 0.1]),
    "Shrek":             np.array([0.25, 0.85, 0.15]),
    "Szeregowiec Ryan":  np.array([0.6, 0.1, 0.7]),
}

def semantic_search(query_vec, database, top_k=3):
    """Wyszukuje top_k najbliższych filmów na podstawie podobieństwa cosinusowego."""
    scores = []
    
    # Obliczamy długość (normę) wektora zapytania raz przed pętlą
    query_norm = np.linalg.norm(query_vec)
    
    for title, doc_vec in database.items():
        # Obliczamy iloczyn skalarny (dot product)
        dot_product = np.dot(query_vec, doc_vec)
        
        # Obliczamy długość wektora dokumentu (filmu)
        doc_norm = np.linalg.norm(doc_vec)
        
        # Wyliczamy podobieństwo cosinusowe (zabezpieczając przed dzieleniem przez zero)
        if query_norm == 0 or doc_norm == 0:
            similarity = 0.0
        else:
            similarity = dot_product / (query_norm * doc_norm)
            
        scores.append((title, similarity))
    
    # Sortujemy wyniki malejąco według obliczonego podobieństwa
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Zwracamy tylko wybraną liczbę najlepszych trafień
    return scores[:top_k]

# Definiujemy wektor zapytania (reprezentujący np. klimaty sci-fi i akcji)
query = np.array([0.7, 0.3, 0.8])

# Uruchamiamy wyszukiwanie semantyczne
results = semantic_search(query, filmy, top_k=3)

# Wyświetlamy sformatowane wyniki w terminalu
print("--- TOP 3 NAJBARDZIEJ PODOBNE FILMY ---")
for title, sim in results:
    print(f"  * {title}: {sim:.3f}")