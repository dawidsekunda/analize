import streamlit as st
import pandas as pd
from analize.data_loader import load_all

# Page config
st.set_page_config(
    page_title="⚽ Football Analyzer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("⚽ Football Analyzer")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Nawigacja",
    ["🏠 Strona główna", "📊 Tabela ligowa", "🏆 Klasyfikacja kanadyjska", 
     "👥 Zawodnicy", "🎯 Top strzelcy", "📈 Statystyki meczów"]
)

# Load data (cached)
@st.cache_data
def load_football_data():
    return load_all()

data = load_football_data()
matches = data['matches']
players = data['players']
performances = data['performances']

# ============== HOME PAGE ==============
if page == "🏠 Strona główna":
    st.title("⚽ Football Analyzer Dashboard")
    st.markdown("Interaktywna analiza danych meczów i zawodników")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Liczba meczów", len(matches))
    with col2:
        st.metric("Liczba zawodników", len(players))
    with col3:
        st.metric("Liczba drużyn", matches['home_team'].nunique())
    with col4:
        total_goals = matches['home_score'].sum() + matches['away_score'].sum()
        st.metric("Razem goli", int(total_goals))
    
    st.markdown("---")
    st.subheader("Ostatnie mecze")
    st.dataframe(matches.tail(5), use_container_width=True)

# ============== LEAGUE TABLE ==============
elif page == "📊 Tabela ligowa":
    st.title("📊 Tabela ligowa (3 pkt za wygraną, 1 za remis)")
    
    # Calculate standings
    df = matches.copy()
    for c in ['home_score', 'away_score']:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
    
    def result_row(r):
        h, a = r['home_score'], r['away_score']
        if h > a:
            return 3, 0
        if h < a:
            return 0, 3
        return 1, 1
    
    pts = df.apply(lambda row: pd.Series(result_row(row), index=['home_points','away_points']), axis=1)
    df = pd.concat([df, pts], axis=1)
    
    home_stats = df.groupby('home_team').agg(
        played_home=('match_id','count'),
        wins_home=('home_points', lambda s: (s==3).sum()),
        draws_home=('home_points', lambda s: (s==1).sum()),
        losses_home=('home_points', lambda s: (s==0).sum()),
        goals_for_home=('home_score','sum'),
        goals_against_home=('away_score','sum'),
        points_home=('home_points','sum'),
    ).rename_axis('team').reset_index()
    
    away_stats = df.groupby('away_team').agg(
        played_away=('match_id','count'),
        wins_away=('away_points', lambda s: (s==3).sum()),
        draws_away=('away_points', lambda s: (s==1).sum()),
        losses_away=('away_points', lambda s: (s==0).sum()),
        goals_for_away=('away_score','sum'),
        goals_against_away=('home_score','sum'),
        points_away=('away_points','sum'),
    ).rename_axis('team').reset_index()
    
    table = pd.merge(home_stats, away_stats, on='team', how='outer').fillna(0)
    
    table['played'] = table['played_home'] + table['played_away']
    table['wins'] = table['wins_home'] + table['wins_away']
    table['draws'] = table['draws_home'] + table['draws_away']
    table['losses'] = table['losses_home'] + table['losses_away']
    table['goals_for'] = table['goals_for_home'] + table['goals_for_away']
    table['goals_against'] = table['goals_against_home'] + table['goals_against_away']
    table['goal_diff'] = table['goals_for'] - table['goals_against']
    table['points'] = table['points_home'] + table['points_away']
    
    standings = table[['team','played','wins','draws','losses','goals_for','goals_against','goal_diff','points']]
    standings = standings.sort_values(by=['points','goal_diff','goals_for'], ascending=[False,False,False]).reset_index(drop=True)
    standings.insert(0, 'position', range(1, len(standings)+1))
    
    # Display with styling
    st.dataframe(
        standings.style.background_gradient(subset=['points'], cmap='RdYlGn'),
        use_container_width=True,
        hide_index=True
    )
    
    # Download CSV
    csv = standings.to_csv(index=False)
    st.download_button(
        label="📥 Pobierz jako CSV",
        data=csv,
        file_name="standings.csv",
        mime="text/csv"
    )

# ============== CANADIAN CLASSIFICATION ==============
elif page == "🏆 Klasyfikacja kanadyjska":
    st.title("🏆 Klasyfikacja kanadyjska (gole + asysty)")
    
    perf = performances.copy()
    players_sel = players.copy()
    
    merged = perf.merge(players_sel[['player_id', 'player_name', 'team']], on='player_id', how='left')
    merged['points'] = merged['goals'] + merged['assists']
    
    results = merged.groupby(['player_id', 'player_name', 'team'])[['goals', 'assists', 'points']].sum().reset_index()
    results = results.sort_values(by=['points', 'goals'], ascending=False)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        top_player = results.iloc[0]
        st.metric("🥇 Lider", top_player['player_name'], f"{int(top_player['points'])} pkt")
    with col2:
        st.metric("Najlepszy gol strzelacz", results.iloc[0]['player_name'], f"{int(results.iloc[0]['goals'])} goli")
    with col3:
        st.metric("Najlepszy asystent", results.nlargest(1, 'assists').iloc[0]['player_name'], 
                 f"{int(results.nlargest(1, 'assists').iloc[0]['assists'])} asyst")
    
    st.markdown("---")
    
    # Filter by team
    teams = ['Wszystkie'] + sorted(results['team'].unique().tolist())
    selected_team = st.selectbox("Filtruj po drużynie:", teams)
    
    if selected_team != 'Wszystkie':
        results_filtered = results[results['team'] == selected_team]
    else:
        results_filtered = results
    
    # Display table
    st.dataframe(
        results_filtered.style.background_gradient(subset=['points'], cmap='YlOrRd'),
        use_container_width=True,
        hide_index=True
    )
    
    # Download CSV
    csv = results_filtered.to_csv(index=False)
    st.download_button(
        label="📥 Pobierz jako CSV",
        data=csv,
        file_name="canadian_classification.csv",
        mime="text/csv"
    )

# ============== PLAYERS ==============
elif page == "👥 Zawodnicy":
    st.title("👥 Baza zawodników")
    
    # Search
    search = st.text_input("🔍 Szukaj po nazwie:", "")
    
    if search:
        filtered_players = players[players['player_name'].str.contains(search, case=False, na=False)]
    else:
        filtered_players = players
    
    st.dataframe(filtered_players, use_container_width=True, hide_index=True)
    
    # Stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Razem zawodników", len(filtered_players))
    with col2:
        st.metric("Drużyn", filtered_players['team'].nunique())
    with col3:
        st.metric("Krajowości", filtered_players['nationality'].nunique())

# ============== TOP SCORERS ==============
elif page == "🎯 Top strzelcy":
    st.title("🎯 Top strzelcy")
    
    top_scorers = performances.groupby('player_id', as_index=False)['goals'].sum().sort_values('goals', ascending=False)
    top_scorers = top_scorers.merge(players[['player_id', 'player_name', 'team']], on='player_id')
    
    # Limit selection
    limit = st.slider("Pokaż top:", 5, 50, 10)
    top_scorers_limited = top_scorers.head(limit)
    
    # Bar chart
    st.bar_chart(data=top_scorers_limited.set_index('player_name')['goals'])
    
    # Table
    st.markdown("---")
    st.dataframe(top_scorers_limited, use_container_width=True, hide_index=True)

# ============== MATCH STATS ==============
elif page == "📈 Statystyki meczów":
    st.title("📈 Statystyki meczów")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Średnie gole na mecz")
        avg_goals_home = matches['home_score'].mean()
        avg_goals_away = matches['away_score'].mean()
        
        chart_data = pd.DataFrame({
            'Typ': ['U siebie', 'Na wyjeździe'],
            'Średnie gole': [avg_goals_home, avg_goals_away]
        })
        st.bar_chart(chart_data.set_index('Typ'))
    
    with col2:
        st.subheader("Rozkład wyników")
        matches['result'] = matches.apply(
            lambda x: 'Wygrana gospodarza' if x['home_score'] > x['away_score'] 
            else ('Wygrana gościa' if x['home_score'] < x['away_score'] else 'Remis'),
            axis=1
        )
        result_counts = matches['result'].value_counts()
        st.bar_chart(result_counts)
    
    st.markdown("---")
    st.subheader("Wszystkie mecze")
    st.dataframe(matches, use_container_width=True, hide_index=True)

st.sidebar.markdown("---")
st.sidebar.info("⚽ Football Analyzer v1.0\nDarmowa analiza danych piłkarskich")
