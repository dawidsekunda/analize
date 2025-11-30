import sys
from tabulate import tabulate
import pandas as pd

from analize.data_loader import load_all


def print_df(df: pd.DataFrame, limit: int = 20):
    if df.empty:
        print('(no rows)')
        return
    print(tabulate(df.head(limit), headers='keys', tablefmt='github', showindex=False))


def show_menu():
    print('\n--- Analiza meczów — CLI ---')
    print('1) Pokaż pierwsze mecze')
    print('2) Pokaż pierwszych zawodników')
    print('3) Pokaż top strzelców')
    print('4) Pokaż statystyki zawodnika (po player_id)')
    print('5) Zapytanie pandas (np. performances[performances.goals > 0])')
    print('6) Zapisz wynik ostatniego zapytania do CSV')
    print('0) Wyjście')


def main():
    data = load_all()
    last_df = None
    while True:
        show_menu()
        choice = input('Wybór: ').strip()
        if choice == '1':
            print_df(data['matches'])
            last_df = data['matches']
        elif choice == '2':
            print_df(data['players'])
            last_df = data['players']
        elif choice == '3':
            perf = data['performances']
            if 'goals' in perf.columns:
                agg = perf.groupby('player_id', as_index=False)['goals'].sum().sort_values('goals', ascending=False)
                print_df(agg)
                last_df = agg
            else:
                print('Brak kolumny goals w performances')
        elif choice == '4':
            pid = input('player_id: ').strip()
            df = data['performances'][data['performances']['player_id'] == pid]
            if df.empty:
                print('Brak danych dla', pid)
            else:
                print_df(df)
            last_df = df
        elif choice == '5':
            expr = input('Wprowadź wyrażenie (użyj names: matches, players, performances):\n> ')
            try:
                matches = data['matches']
                players = data['players']
                performances = data['performances']
                # Evaluate in a restricted local namespace
                local_ns = {'matches': matches, 'players': players, 'performances': performances, 'pd': pd}
                result = eval(expr, {}, local_ns)
                if isinstance(result, pd.DataFrame):
                    print_df(result)
                    last_df = result
                else:
                    print('Wynik:', result)
                    last_df = None
            except Exception as e:
                print('Błąd podczas ewaluacji zapytania:', e)
        elif choice == '6':
            if last_df is None:
                print('Brak wyniku do zapisania')
            else:
                path = input('Ścieżka pliku CSV do zapisu (np. output.csv): ').strip()
                try:
                    last_df.to_csv(path, index=False)
                    print('Zapisano do', path)
                except Exception as e:
                    print('Błąd zapisu:', e)
        elif choice == '0':
            print('Do widzenia')
            sys.exit(0)
        else:
            print('Nieznana opcja')


if __name__ == '__main__':
    main()
