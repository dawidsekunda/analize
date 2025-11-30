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
