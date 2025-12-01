import os
import sys

# --- DANE DO DODANIA ---

new_players = """
P013,Kacper Tobiasz,Legia Warszawa,Goalkeeper,21,Poland
P014,Mikael Ishak,Lech Poznań,Forward,31,Sweden
P015,Kamil Grosicki,Pogoń Szczecin,Midfielder,36,Poland
P016,Erik Exposito,Śląsk Wrocław,Forward,28,Spain
P017,Bartosz Salamon,Lech Poznań,Defender,33,Poland
P018,Rafał Augustyniak,Legia Warszawa,Defender,30,Poland
P019,Efthymios Koulouris,Pogoń Szczecin,Forward,29,Greece
P020,Kacper Chodyna,Zagłębie Lubin,Midfielder,25,Poland
P021,Sokratis Dioudis,Zagłębie Lubin,Goalkeeper,31,Greece
P022,Rafał Leszczyński,Śląsk Wrocław,Goalkeeper,32,Poland
P023,Alan Uryga,Wisła Kraków,Defender,30,Poland
P024,Angel Rodado,Wisła Kraków,Forward,27,Spain
P025,Linus Wahlqvist,Pogoń Szczecin,Defender,27,Sweden
"""

new_matches = """
M011,2025-10-19,Lech Poznań,Śląsk Wrocław,2,0,Ekstraklasa,2025/2026,Stadion Poznań
M012,2025-10-20,Legia Warszawa,Pogoń Szczecin,1,1,Ekstraklasa,2025/2026,Stadion Wojska Polskiego
M013,2025-10-20,Zagłębie Lubin,Wisła Kraków,2,1,Ekstraklasa,2025/2026,Stadion Lubin
M014,2025-10-27,Wisła Kraków,Lech Poznań,1,4,Ekstraklasa,2025/2026,Stadion Wisły
M015,2025-10-27,Śląsk Wrocław,Legia Warszawa,0,2,Ekstraklasa,2025/2026,Stadion Wrocław
M016,2025-10-28,Pogoń Szczecin,Zagłębie Lubin,3,0,Ekstraklasa,2025/2026,Stadion Pogoni
M017,2025-11-03,Lech Poznań,Zagłębie Lubin,1,1,Ekstraklasa,2025/2026,Stadion Poznań
M018,2025-11-04,Legia Warszawa,Wisła Kraków,3,1,Ekstraklasa,2025/2026,Stadion Wojska Polskiego
M019,2025-11-04,Śląsk Wrocław,Pogoń Szczecin,1,2,Ekstraklasa,2025/2026,Stadion Wrocław
M020,2025-11-10,Pogoń Szczecin,Lech Poznań,0,0,Ekstraklasa,2025/2026,Stadion Pogoni
"""

new_performances = """
M011,P014,90,12,2,85.71,4,2,50.00,2,0,0,0,0,0
M011,P001,88,45,5,90.00,1,0,0.00,0,1,0,0,2,1
M011,P016,90,10,4,71.42,2,0,0.00,0,0,1,0,1,0
M012,P003,90,55,10,84.61,2,1,50.00,0,1,1,0,3,2
M012,P015,85,30,8,78.94,1,1,100.00,1,0,0,0,0,1
M012,P019,90,15,5,75.00,3,1,33.33,0,0,0,0,1,0
M013,P020,90,40,4,90.90,2,2,100.00,1,1,0,0,2,2
M013,P024,90,20,5,80.00,4,2,50.00,1,0,0,0,0,0
M014,P014,90,18,3,85.71,5,4,80.00,3,0,0,0,0,0
M014,P011,75,10,2,83.33,1,1,100.00,1,1,0,0,0,0
M014,P023,90,40,2,95.23,0,0,0.00,0,0,1,0,4,1
M015,P003,90,60,5,92.30,1,0,0.00,0,1,0,0,2,2
M015,P018,90,50,3,94.33,0,0,0.00,0,0,0,0,5,3
M015,P016,90,12,6,66.67,1,0,0.00,0,0,1,0,0,0
M016,P015,88,35,4,89.74,2,2,100.00,1,2,0,0,1,1
M016,P019,90,20,3,86.95,3,2,66.67,2,0,0,0,0,0
M017,P017,90,55,4,93.22,1,0,0.00,0,0,1,0,6,4
M017,P020,90,42,8,84.00,2,1,50.00,1,0,0,0,2,1
M018,P003,90,65,7,90.27,3,2,66.67,1,1,0,0,2,1
M018,P013,90,15,0,100.00,0,0,0.00,0,0,0,0,0,0
M018,P024,90,18,4,81.81,2,1,50.00,1,0,0,0,1,0
M019,P015,90,28,5,84.84,1,1,100.00,1,0,0,0,0,2
M019,P022,90,10,1,90.90,0,0,0.00,0,0,0,0,0,0
M020,P015,90,22,6,78.57,1,0,0.00,0,0,1,0,1,0
M020,P014,90,14,3,82.35,2,0,0.00,0,0,0,0,1,0
"""

def find_data_folder():
    """Szuka folderu data w obecnym katalogu lub w podkatalogu analize"""
    if os.path.exists('data'):
        return 'data'
    elif os.path.exists(os.path.join('analize', 'data')):
        return os.path.join('analize', 'data')
    else:
        return None

def append_to_file(folder, filename, data_string):
    path = os.path.join(folder, filename)
    
    if not os.path.exists(path):
        print(f"BŁĄD: Nie znaleziono pliku: {path}")
        return

    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + data_string.strip())
    
    print(f"Sukces: Dodano nowe wiersze do {filename}")

if __name__ == '__main__':
    print("--- Aktualizacja Bazy Danych ---")
    
    # 1. Znajdź folder
    data_folder = find_data_folder()
    
    if not data_folder:
        print("CRITICAL ERROR: Nie znaleziono folderu 'data' ani 'analize/data'!")
        print(f"Program uruchomiony w: {os.getcwd()}")
        print("Sprawdź strukturę folderów.")
    else:
        print(f"Znaleziono folder danych: {data_folder}")
        
        # 2. Aktualizuj pliki (używamy Twoich nazw)
        append_to_file(data_folder, 'players.csv', new_players)
        
        # Uwaga: Napisałeś 'mateches.csv' w czacie, ale zakładam, że plik to 'matches.csv'. 
        # Jeśli masz literówkę w nazwie pliku na dysku, zmień poniżej 'matches.csv' na 'mateches.csv'
        append_to_file(data_folder, 'matches.csv', new_matches)
        
        # Tutaj była zmiana: player_performances.csv zamiast performances.csv
        append_to_file(data_folder, 'player_performances.csv', new_performances)
        
        print("Zakończono.")