"""Ukryte rozwiązania zadań — poproś mnie o wyjaśnienie.

Plik zawiera funkcje, które ładują dane i zwracają wyniki dla ćwiczeń z `exercises.md`.
Nie usuwaj pliku jeśli chcesz żebym mógł później automatycznie sprawdzić Twoje rozwiązania.
"""
from analize.data_loader import load_all


def avg_pass_accuracy_per_player():
    data = load_all()
    perf = data['performances']
    if 'pass_accuracy' not in perf.columns:
        return None
    res = perf.groupby('player_id', as_index=False)['pass_accuracy'].mean().sort_values('pass_accuracy', ascending=False)
    return res


def top_scorers(n=5):
    data = load_all()
    perf = data['performances']
    if 'goals' not in perf.columns:
        return None
    res = perf.groupby('player_id', as_index=False)['goals'].sum().sort_values('goals', ascending=False).head(n)
    return res


def team_avg_pass_accuracy():
    data = load_all()
    players = data['players']
    perf = data['performances']
    merged = perf.merge(players[['player_id', 'team']], on='player_id', how='left')
    if 'pass_accuracy' not in merged.columns:
        return None
    res = merged.groupby('team', as_index=False)['pass_accuracy'].mean().sort_values('pass_accuracy', ascending=False)
    return res


def single_game_most_interceptions():
    data = load_all()
    perf = data['performances']
    if 'interceptions' not in perf.columns:
        return None
    return perf.sort_values('interceptions', ascending=False).head(1)


def corr_passes_assists():
    data = load_all()
    perf = data['performances']
    if not {'passes_completed', 'assists'}.issubset(set(perf.columns)):
        return None
    df = perf[['passes_completed', 'assists']].dropna()
    return df['passes_completed'].corr(df['assists'])


if __name__ == '__main__':
    print('To jest ukryty moduł z rozwiązaniami. Importuj funkcje i poproś mnie o wyjaśnienie.')
