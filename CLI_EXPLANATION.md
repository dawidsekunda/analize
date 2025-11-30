# Wyjaśnienie cli.py — Krok po kroku

CO ROBI cli.py?
───────────────
cli.py to interaktywny program (CLI = Command Line Interface), który umożliwia:

- Załadowanie danych z CSV (matches, players, performances)
- Wyświetlenie danych w przyjaznym formacie (tabelę)
- Wykonanie zapytań na danych (filtrowanie, agregacja itp.)
- Zapisanie wyników do pliku CSV

STRUKTURA PLIKU:
────────────────

1. IMPORIY
   from analize.data_loader import load_all — ładowanie danych
   from tabulate import tabulate — formatowanie tabel
   import pandas as pd — przetwarzanie danych

2. FUNKCJA print_df(df, limit=20)
   Wyświetla DataFrame w ładnym formacie (tabela)

   Logika:

   ```
   if df.empty:
       print('(no rows)')
   else:
       tabulate(df.head(limit), headers='keys', tablefmt='github')
   ```

3. FUNKCJA show_menu()
   Wypisuje menu z 7 opcjami (0-6)
   Nie przyjmuje parametrów, nie zwraca wartości

4. FUNKCJA main()
   Główna pętla programu

   Logika:

   ```
   data = load_all()  # Załaduj wszystkie dane
   last_df = None     # Cache dla wyniku (do opcji 6)

   while True:  # Nieskończona pętla
       show_menu()               # Pokaż menu
       choice = input('Wybór: ') # Wczytaj od użytkownika

       if choice == '1':
           # Pokaż mecze
       elif choice == '2':
           # Pokaż zawodników
       ... itd dla opcji 3-6 ...
       elif choice == '0':
           sys.exit(0)  # Wyjście
       else:
           print('Nieznana opcja')  # Błąd
   ```

PRZEPŁYW PROGRAMU (Flow):
────────────────────────

START
│
├─→ if **name** == '**main**': main()
│
├─→ load_all() [załaduj matches, players, performances]
│
├─→ PĘTLA while True:
│ │
│ ├─→ show_menu() [pokaż opcje]
│ │
│ ├─→ input('Wybór: ') [czekaj na wpisanie numeru]
│ │
│ ├─→ if choice == '1': print_df(matches) [opcja 1]
│ ├─→ if choice == '2': print_df(players) [opcja 2]
│ ├─→ if choice == '3': aggregate goals [opcja 3]
│ ├─→ if choice == '4': filter by player_id [opcja 4]
│ ├─→ if choice == '5': eval custom expr [opcja 5]
│ ├─→ if choice == '6': save to CSV [opcja 6]
│ ├─→ if choice == '0': sys.exit(0) [wyjście]
│ │
│ └─→ Powrót do show_menu()
│
KONIEC

SZCZEGÓŁOWE WYJAŚNIENIE KAŻDEJ OPCJI:
──────────────────────────────────────

1. POKAŻ PIERWSZE MECZE
   ─────────────────────
   Co się dzieje:

   - data['matches'] to DataFrame z kolumnami: match_id, date, home_team, away_team, home_score, ...
   - print_df() bierze df.head(20) — pierwsze 20 wierszy
   - tabulate() formatuje to jako tabelę do wyświetlenia w terminalu
   - last_df = data['matches'] — zapamiętaj wynik (na wypadek, gdybyś chciał go zapisać w opcji 6)

2. POKAŻ PIERWSZYCH ZAWODNIKÓW
   ───────────────────────────
   Co się dzieje:

   - data['players'] to DataFrame z kolumnami: player_id, player_name, team, position, age, ...
   - print_df() wyświetla pierwsze 20 graczy
   - last_df = data['players'] — zapamiętaj wynik

3. POKAŻ TOP STRZELCÓW
   ──────────────────
   Co się dzieje:

   - perf = data['performances'] — bierz dane występów zawodników
   - perf.groupby('player_id', as_index=False)['goals'].sum()
     → Grupuj po player_id, sumuj kolumnę 'goals'
     → Wynik: DataFrame z player_id i suma_goli
   - .sort_values('goals', ascending=False)
     → Sortuj po 'goals' malejąco (największe liczby na górze)
   - print_df(agg) — wyświetl zarangowany ranking
   - last_df = agg — zapamiętaj wynik

4. POKAŻ STATYSTYKI ZAWODNIKA
   ──────────────────────────
   Co się dzieje:

   - Pytamy: "player_id: " i czekamy na wpisanie, np. "P001"
   - df = data['performances']data['performances']['player_id'] == pid]
     → Filtruj: weź TYLKO wiersze gdzie player_id == 'P001'
   - Wyświetl wszystkie mecze zawodnika, jego statystyki
   - last_df = df — zapamiętaj wynik

5. ZAPYTANIE PANDAS (Custom Expression)
   ────────────────────────────────────
   Co się dzieje:

   - Pytamy: "Wprowadź wyrażenie: " i czekamy na wpisanie, np:
     performances[performances.goals > 0]
     lub:
     matches[matches.home_score > 2]
   - Przygotowujemy namespace (dostępne zmienne):
     local_ns = {
     'matches': data['matches'],
     'players': data['players'],
     'performances': data['performances'],
     'pd': pd (moduł pandas)
     }
   - eval(expr, {}, local_ns) — ewaluuj wyrażenie w tym namespace
     → Upewnij się, że nie ma dostępu do niebezpiecznych funkcji
   - Jeśli wynik to DataFrame: wyświetl tabelą
   - Jeśli wynik to liczba/tekst: wypisz wartość
   - try/except — obsłuż błędy (jeśli wyrażenie jest nieprawidłowe)
   - last_df = result — zapamiętaj (jeśli DataFrame)

6. ZAPISZ WYNIK DO CSV
   ───────────────────
   Co się dzieje:

   - Pytamy: "Ścieżka pliku CSV: " i czekamy na wpisanie, np. "results.csv"
   - Jeśli last_df jest None (pusty):
     → Wypisz: "Brak wyniku do zapisania"
   - W przeciwnym razie:
     → last_df.to_csv(path, index=False)
     → Zapisz DataFrame do pliku CSV
     → Wypisz: "Zapisano do results.csv"

7. WYJŚCIE
   ───────
   Co się dzieje:
   - sys.exit(0) — zamknij program
   - 0 = normalny koniec (brak błędu)

ZMIENNE WAŻNE:
──────────────

data = load_all()
Dict zawierający:
{
'matches': DataFrame,
'players': DataFrame,
'performances': DataFrame
}

last_df = None
Cache przechowujący ostatni DataFrame wyświetlony
Używany w opcji 6 do zapisania wyniku

FUNKCJE Z BIBLIOTEK:
──────────────────

pd.read_csv(path)
Załaduj plik CSV do DataFrame'a

df.head(20)
Weź pierwsze 20 wierszy z DataFrame'a

df.groupby('kolumna')
Grupuj wiersze po wartościach w kolumnie

df['kolumna'].sum()
Sumuj wartości w kolumnie

df[df['kolumna'] == 'wartość']
Filtruj: weź TYLKO wiersze gdzie kolumna == wartość

df.sort_values('kolumna', ascending=False)
Sortuj po kolumnie malejąco (False = zmniejszając)

df.to_csv(path, index=False)
Zapisz DataFrame do pliku CSV

tabulate(data, headers='keys', tablefmt='github')
Formatuj dane jako ładną tabelę

eval(expression, globals, locals)
Ewaluuj wyrażenie Pythona (tutaj: pandas expression)

PRZYKŁAD SESJI W PRAKTYCE:
────────────────────────

$ .\.venv\Scripts\python.exe -m analize.cli

--- Analiza meczów — CLI ---

1. Pokaż pierwsze mecze
2. Pokaż pierwszych zawodników
3. Pokaż top strzelców
4. Pokaż statystyki zawodnika (po player_id)
5. Zapytanie pandas (np. performances[performances.goals > 0])
6. Zapisz wynik ostatniego zapytania do CSV
7. Wyjście
   Wybór: 3

| player_id | goals |
| --------- | ----- |
| P002      | 3     |
| P001      | 1     |
| P008      | 1     |

--- Analiza meczów — CLI ---
...
Wybór: 5
Wprowadź wyrażenie (użyj names: matches, players, performances):

> performances[performances.goals > 0]

| match_id | player_id | minutes_played | passes_completed | ... goals |
| -------- | --------- | -------------- | ---------------- | --------- |
| M001     | P002      | 75             | 24               | ... 2     |
| M002     | P005      | 88             | 18               | ... 1     |
| M004     | P002      | 90             | 30               | ... 1     |

--- Analiza meczów — CLI ---
...
Wybór: 6
Ścieżka pliku CSV do zapisu (np. output.csv): my_goals.csv
Zapisano do my_goals.csv

--- Analiza meczów — CLI ---
...
Wybór: 0
Do widzenia
$
