# CLI Diagram — Przepływ działania skryptu analize/cli.py

```
┌─────────────────────────────────────────────────────────────────────┐
│ START: python -m analize.cli                                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │ main() — pętla programu      │
              │ • load_all() załaduje dane   │
              │ • last_df = None (cache)     │
              └──────────┬───────────────────┘
                         │
                         ▼
              ╔══════════════════════════════╗
              ║  show_menu() — wyświetl menu ║
              ╚═════════════┬════════════════╝
                            │
                            ▼
              ┌──────────────────────────────┐
              │ Wczytaj od użytkownika:      │
              │ input('Wybór: ')             │
              └──────┬───────────────────────┘
                     │
    ┌────────────────┼────────────────┬──────────────┬──────────────┬──────────┐
    │                │                │              │              │          │
    ▼                ▼                ▼              ▼              ▼          ▼
  (1)            (2)              (3)            (4)             (5)        (6)
┌──────┐    ┌──────────┐    ┌────────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐
│Show  │    │Show      │    │Aggregate  │  │Filter by │  │eval()    │  │Save  │
│      │    │          │    │           │  │player_id │  │custom    │  │last_ │
│Matches    │Players   │    │Top Goals  │  │          │  │expr      │  │df   │
│      │    │          │    │by player  │  │          │  │          │  │CSV  │
└──┬───┘    └───┬──────┘    └────┬──────┘  └────┬─────┘  └────┬─────┘  └─┬────┘
   │            │                 │             │             │         │
   └─ print_df()─┴─ print_df() ──┴─────────────┴─────────────┴─────────┘
   │            │                 │             │             │         │
   ▼            ▼                 ▼             ▼             ▼         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Obsługa wyniku:                                                         │
│ • print_df(df) — sformatuj i wyświetl DataFrame (tabela)                │
│ • last_df = df — zapisz wynik w cache (dla opcji 6)                     │
│ • Obsługa błędów (try/except dla opcji 5)                               │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                    ▼▼▼ „Wciśnij Enter" ▼▼▼
                             │
                             ▼
                    ┌─────────────────────┐
                    │ Powrót do show_menu()
                    │ (pętla while True)  │
                    └──────────┬──────────┘
                               │
                    ───────────┘
                    │
                    ▼
                  (0)
              ┌─────────────┐
              │ EXIT        │
              │ Wyjście     │
              │ sys.exit(0) │
              └─────────────┘
```

SZCZEGÓŁOWY OPIS OPCJI:
═════════════════════════════════════════════════════════════════════

Opcja 1) POKAŻ PIERWSZE MECZE
─────────────────────────────
Input: Wciśnij "1" w menu
Proces: data['matches'] zawiera DataFrame z meczami
print_df() formatuje dane i wyświetla pierwsze 20 wierszy
Output: Tabela meczów (match_id, date, teams, scores itp.)
Cache: last_df = data['matches'] — zostaje do opcji 6

Opcja 2) POKAŻ PIERWSZYCH ZAWODNIKÓW
────────────────────────────────────
Input: Wciśnij "2" w menu
Proces: data['players'] zawiera DataFrame z graczami
print_df() formatuje i wyświetla pierwsze 20 wierszy
Output: Tabela graczy (player_id, name, team, position, age itp.)
Cache: last_df = data['players'] — zostaje do opcji 6

Opcja 3) POKAŻ TOP STRZELCÓW
─────────────────────────────
Input: Wciśnij "3" w menu
Proces: 1. Załaduj: perf = data['performances'] 2. Grupuj po player_id i sumuj kolumnę 'goals' 3. Sortuj malejąco (najwyższe gole na górze) 4. Wyświetl tabelę
Output: Ranking graczy po liczbie goli
Cache: last_df = agg — wynik agregacji (do opcji 6)

Equivalent:
perf.groupby('player_id', as_index=False)['goals'].sum() \
 .sort_values('goals', ascending=False)

Opcja 4) POKAŻ STATYSTYKI ZAWODNIKA (po player_id)
──────────────────────────────────────────────────
Input: Wciśnij "4", potem wpisz player_id (np. "P001")
Proces: 1. Załaduj: perf = data['performances'] 2. Filtruj wiersze gdzie player_id = wpisana wartość 3. Wyświetl wszystkie mecze zawodnika i jego statystyki
Output: Tabela występów jednego zawodnika (minutes, passes, goals itp.)
Cache: last_df = df — wiersze zawodnika (do opcji 6)

Equivalent:
data['performances']data['performances']['player_id'] == 'P001']

Opcja 5) ZAPYTANIE PANDAS — CUSTOM WYRAŻENIE
──────────────────────────────────────────────
Input: Wciśnij "5", potem wpisz wyrażenie pandas (np.)
performances[performances.goals > 0]
players.merge(performances.groupby('player_id')['assists'].sum())

Proces: 1. Przygotuj dostępne zmienne: - matches, players, performances (DataFrame'y) - pd (moduł pandas) 2. Ewaluuj wyrażenie użytkownika w bezpiecznej przestrzeni 3. Jeśli wynik = DataFrame: wyświetl tabelą
Jeśli wynik = liczba/teksty: wyświetl wartość 4. Obsłuż błędy (TriError, atrybuty, składnia itp.)

Output: Dowolny wynik wyrażenia pandas (DataFrame lub wartość)
Cache: last_df = result (jeśli DataFrame, do opcji 6)

Przykłady wyrażeń:
performances[performances.goals > 0]
→ Wszyscy zawodnicy ze strzelanym golem

    matches[matches.home_score > matches.away_score]
    → Mecze, które wygrał zespół gospodarzy

    performances.groupby('player_id')['passes_completed'].mean()
    → Średnia liczba podań celnych per zawodnik

Opcja 6) ZAPISZ WYNIK DO CSV
─────────────────────────────
Input: Wciśnij "6", potem wpisz ścieżkę pliku (np. "my_results.csv")
Proces: 1. Sprawdzaj: czy last_df jest dostępny (cache nie pusty)? 2. Jeśli pusty: wyświetl komunikat "Brak wyniku" 3. Jeśli dostępny: - last_df.to_csv(path, index=False) - Zapisz DataFrame do pliku CSV - Pokaż komunikat "Zapisano do [path]"
Output: Plik CSV z danymi
Błędy: Obsługa wyjątków (Permission denied, invalid path itp.)

Opcja 0) WYJŚCIE
────────────────
Input: Wciśnij "0"
Proces: sys.exit(0) — zamknij program
Output: (brak) — program się kończy

KLUCZOWE FUNKCJE:
═════════════════════════════════════════════════════════════════════

print_df(df: pd.DataFrame, limit: int = 20)
──────────────────────────────────────────
Parametry: df — DataFrame do wyświetlenia
limit — ile wierszy pokazać (default 20)

Logika: 1. Sprawdzaj: czy DataFrame jest pusty? 2. Jeśli pusty: wyświetl "(no rows)" 3. Jeśli nie: użyj tabulate.tabulate() do formatowania - headers='keys' → kolumny z nazw DataFrame - tablefmt='github' → format tabeli (czytelny) - showindex=False → nie pokazuj indeksu (numeracji)

Efekt: Ładna, czytelna tabela w terminalu

show_menu()
───────────
Parametry: (brak)

Logika: Wypisz menu z wszystkimi opcjami (0-6)

Efekt: Użytkownik widzi, jakie akcje może wykonać

main()
──────
Parametry: (brak)

Logika: 1. Załaduj wszystkie dane: data = load_all() 2. last_df = None (cache dla wyników) 3. Pętla while True: - show_menu() — wyświetl menu - wczytaj wybór użytkownika - Obsłuż każdą opcję (1-6, 0) - Powrót do show_menu()

Efekt: Program działa interaktywnie dopóki użytkownik nie wybierze 0

DATA FLOW (Przepływ danych):
═════════════════════════════════════════════════════════════════════

                      load_all() [data_loader.py]
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          matches.csv   players.csv   performances.csv
                │              │              │
                ▼              ▼              ▼
    pd.read_csv()    pd.read_csv()   pd.read_csv()
                │              │              │
                ▼              ▼              ▼
            DataFrame      DataFrame       DataFrame
          (10 rows)       (12 rows)       (24 rows)
                │              │              │
                └──────────────┼──────────────┘
                               │
                  data = {
                    'matches': DataFrame,
                    'players': DataFrame,
                    'performances': DataFrame
                  }
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
                Opcje 1-5         Opcja 6 — CSV
              (wyświetlanie)      (zapis last_df)

PRZYKŁAD SESJI:
═════════════════════════════════════════════════════════════════════

PS> .\.venv\Scripts\python.exe -m analize.cli

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

...

--- Analiza meczów — CLI ---
...
Wybór: 6
Ścieżka pliku CSV do zapisu (np. output.csv): top_scorers.csv
Zapisano do top_scorers.csv

--- Analiza meczów — CLI ---
...
Wybór: 0
Do widzenia
PS>
