# Ćwiczenia do samodzielnej pracy

Poniżej znajdziesz przykładowe zadania, które możesz rozwiązać używając danych w `data/` i narzędzia w `analize`.

1. Średnia dokładność podań (`pass_accuracy`) dla każdego zawodnika. Posortuj malejąco.

   - Hint: użyj `performances.groupby('player_id')['pass_accuracy'].mean()`

2. Top 5 strzelców w sezonie (suma `goals` po `player_id`).

3. Które drużyny mają najwyższą średnią dokładność podań (łącząc zawodników drużyny)?

4. Znajdź zawodnika z największą liczbą przechwytów (`interceptions`) w pojedynczym meczu.

5. Oblicz korelację między `passes_completed` a `assists` (czy więcej podań daje więcej asyst?).

6. (Ekstra) Zbuduj prosty model regresji (np. sklearn) przewidujący liczbę asyst na podstawie podań i strzałów.

Instrukcja pracy:

- Otwórz `analize/cli.py` i użyj opcji 5 z odpowiednim wyrażeniem pandas, albo otwórz notebook i użyj `analize/data_loader.py`.
- Gdy skończysz, poproś mnie o sprawdzenie — mogę uruchomić rozwiązanie z `analize/solutions/_solutions.py` i wytłumaczyć.
