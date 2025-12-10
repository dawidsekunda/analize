# Analiza danych meczów — narzędzie startowe

Instrukcje szybkie (PowerShell):

1. Stwórz środowisko w katalogu projektu:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r analize\requirements.txt
```

2. Uruchom CLI analizatora:

```powershell
# Możesz uruchomić bezpośrednio plik (ale importy będą działać lepiej
# jeśli folder jest paczką lub uruchomisz jako moduł — poniżej przykład):
python analize\cli.py
```

**Zalecane (uruchom jako moduł):**

```powershell
# Uruchom moduł pakietu — najbezpieczniejsza metoda kiedy jesteś w katalogu projektu
.\.venv\Scripts\python.exe -m analize.cli
```

3. Pliki z danymi powinny znajdować się w folderze `data` (już utworzone):
   `data/matches.csv`, `data/players.csv`, `data/player_performances.csv`.

Zawartość katalogu `analize`:

- `data_loader.py` — funkcje ładujące dane (pandas)
- `cli.py` — prosty interaktywny CLI do zapytań
- `exercises.md` — przykładowe zadania dla Ciebie
- `solutions/_solutions.py` — ukryte rozwiązania (proś mnie o wyjaśnienie)

Chcesz żebym stworzył notebook z przykładami analizy? Napisz "notebook".

---

Alternatywne sposoby uruchomienia (gdy PowerShell blokuje skrypty):

- Opcja C — uruchamianie bez aktywacji (zalecane jeśli nie chcesz zmieniać polityki):

```powershell
# Zainstaluj wymagania bez aktywacji
.\.venv\Scripts\python.exe -m pip install -r analize\requirements.txt

# Uruchom CLI bez aktywacji venv
.\.venv\Scripts\python.exe analize\cli.py
```

- Opcja A — tymczasowy Bypass tylko dla bieżącej sesji (nie wymaga admina):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. \.venv\Scripts\Activate.ps1
```

- Opcja B — trwałe ustawienie dla bieżącego użytkownika (RemoteSigned, bez admina):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
. \.venv\Scripts\Activate.ps1
```

Dlatego przygotowałem helper `run.ps1` w tym katalogu, który tymczasowo ustawi Bypass dla sesji i uruchomi CLI (nie zmienia ustawień systemowych na stałe). Aby go użyć uruchom w PowerShell z katalogu projektu:

```powershell
# Uruchamia analize\run.ps1 — tymczasowy Bypass i start CLI
powershell -ExecutionPolicy Bypass -File .\analize\run.ps1
```

Jeśli chcesz, mogę też dodać wersję dla `cmd.exe` lub rozszerzyć README o FAQ dotyczące ExecutionPolicy.

---

**Demo & Presentation**

Jeśli chcesz pokazać demo na spotkaniu, uruchom Streamlit i otwórz aplikację w przeglądarce:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Jeśli nie chcesz aktywować venv, możesz uruchomić bezpośrednio:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

Poniżej krótkie podglądy (pierwsze 5 wierszy) plików CSV, żebyś mógł szybko sprawdzić strukturę danych bez otwierania plików.

**`data/matches.csv`**

```
match_id,date,home_team,away_team,home_score,away_score,league,season,stadium
M001,2025-08-10,Lech Poznań,Legia Warszawa,2,1,Ekstraklasa,2025/2026,Stadion Poznań
M002,2025-08-17,Wisła Kraków,Pogoń Szczecin,1,3,Ekstraklasa,2025/2026,Stadion Wisły
M003,2025-08-24,Śląsk Wrocław,Zagłębie Lubin,0,0,Ekstraklasa,2025/2026,Stadion Wrocław
M004,2025-09-01,Lech Poznań,Wisła Kraków,3,0,Ekstraklasa,2025/2026,Stadion Poznań
M005,2025-09-07,Legia Warszawa,Śląsk Wrocław,1,2,Ekstraklasa,2025/2026,Stadion Wojska Polskiego
```

**`data/players.csv`**

```
player_id,player_name,team,position,age,nationality
P001,Adam Nowak,Lech Poznań,Midfielder,26,Poland
P002,Jan Kowalski,Lech Poznań,Forward,24,Poland
P003,Piotr Zieliński,Legia Warszawa,Midfielder,28,Poland
P004,Marcin Wójcik,Legia Warszawa,Defender,30,Poland
P005,Marek Kamiński,Wisła Kraków,Forward,22,Poland
```

**`data/player_performances.csv`**

```
match_id,player_id,minutes_played,passes_completed,passes_missed,pass_accuracy,shots,shots_on_target,shot_accuracy,goals,assists,yellow_cards,red_cards,tackles,interceptions
M001,P001,90,58,7,89.23,1,1,100.00,0,1,0,0,3,2
M001,P002,75,24,6,80.00,4,2,50.00,2,0,1,0,1,0
M001,P003,90,61,9,87.14,2,1,50.00,0,0,1,0,4,3
M002,P005,88,18,3,85.71,3,2,66.67,1,0,0,0,0,1
M002,P006,90,40,5,88.89,0,0,0.00,0,0,1,0,5,2
```
