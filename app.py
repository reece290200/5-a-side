import streamlit as st
import itertools

st.set_page_config(page_title="5-a-Side FUT Team Picker", layout="wide")

# --- CSS Styling for FUT-style cards ---
st.markdown("""
<style>
.card {
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 15px;
    color: white;
    text-align: center;
    font-family: 'Arial';
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}
.gold { background: linear-gradient(135deg,#FFD700,#FFA500);}
.silver { background: linear-gradient(135deg,#C0C0C0,#A9A9A9);}
.bronze { background: linear-gradient(135deg,#CD7F32,#A0522D);}
.stat { display: flex; justify-content: space-between; margin: 3px 0; font-size: 14px; }
.team-column { padding: 5px; }
.team-title { font-size: 24px; font-weight: bold; margin-bottom: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("⚽ 5-a-Side FUT Team Generator")

positions = ["GK", "DEF", "MID", "FWD"]

# --- Sidebar: Mode & View ---
mode = st.sidebar.radio("Mode", ["Auto Balance", "Manual Pick"])
view = st.sidebar.radio("View", ["Card View", "Pitch View"])

# --- Player Input ---
st.sidebar.header("Enter 10 Players")
players = []
for i in range(10):
    with st.sidebar.expander(f"Player {i+1}"):
        name = st.text_input("Name", key=f"name_{i}")
        pos = st.selectbox("Position", positions, key=f"pos_{i}")
        attack = st.slider("Attack", 0, 10, 5, key=f"attack_{i}")
        defense = st.slider("Defense", 0, 10, 5, key=f"def_{i}")
        passing = st.slider("Passing", 0, 10, 5, key=f"pass_{i}")
        pace = st.slider("Pace", 0, 10, 5, key=f"pace_{i}")
        physical = st.slider("Physicality", 0, 10, 5, key=f"phys_{i}")
        overall = (attack + defense + passing + pace + physical) / 5
        players.append({
            "name": name if name else f"Player {i+1}",
            "pos": pos,
            "attack": attack,
            "defense": defense,
            "passing": passing,
            "pace": pace,
            "physical": physical,
            "overall": overall
        })

# --- Helper functions ---
def card_color(overall):
    if overall >= 8: return "gold"
    elif overall >= 5: return "silver"
    else: return "bronze"

def render_card(player):
    color = card_color(player["overall"])
    st.markdown(f"""
    <div class="card {color}">
        <h3>{player['name']}</h3>
        <h4>{player['pos']} – ⭐ {round(player['overall'],1)}</h4>
        <div class="stat">⚡ Attack: {player['attack']}</div>
        <div class="stat">🛡 Defense: {player['defense']}</div>
        <div class="stat">🎯 Passing: {player['passing']}</div>
        <div class="stat">💨 Pace: {player['pace']}</div>
        <div class="stat">💪 Physical: {player['physical']}</div>
    </div>
    """, unsafe_allow_html=True)

def render_pitch(team_a, team_b):
    st.subheader("📋 Pitch View")
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        st.markdown("### 🔵 Team A")
        for p in team_a: render_card(p)
    with col3:
        st.markdown("### 🔴 Team B")
        for p in team_b: render_card(p)
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Football_pitch_plain.svg/600px-Football_pitch_plain.svg.png", use_column_width=True)

# --- Team Generation ---
def auto_balance(players):
    best_diff = float("inf")
    best_split = None
    for combo in itertools.combinations(players,5):
        team_a = list(combo)
        team_b = [p for p in players if p not in team_a]
        total_a = sum(p["overall"] for p in team_a)
        total_b = sum(p["overall"] for p in team_b)
        diff = abs(total_a - total_b)
        if diff < best_diff:
            best_diff = diff
            best_split = (team_a, team_b)
    return best_split, best_diff

# --- Main App Logic ---
if mode == "Auto Balance":
    if st.sidebar.button("Generate Teams"):
        if len(players) == 10:
            team_a, team_b, = auto_balance(players)[0]
            diff = auto_balance(players)[1]
            if view == "Card View":
                col1,col2 = st.columns(2)
                with col1: st.markdown("### 🔵 Team A"); [render_card(p) for p in team_a]
                with col2: st.markdown("### 🔴 Team B"); [render_card(p) for p in team_b]
            else:
                render_pitch(team_a, team_b)
            st.subheader("⚖️ Balance Check")
            st.success(f"Difference in team strength: {round(diff,1)} points")
        else:
            st.warning("Enter all 10 players")
else:
    st.sidebar.subheader("Assign Players to Team A")
    team_a_names = st.sidebar.multiselect("Team A Players", [p["name"] for p in players])
    team_a = [p for p in players if p["name"] in team_a_names]
    team_b = [p for p in players if p["name"] not in team_a_names]
    if view == "Card View":
        col1,col2 = st.columns(2)
        with col1: st.markdown("### 🔵 Team A"); [render_card(p) for p in team_a]
        with col2: st.markdown("### 🔴 Team B"); [render_card(p) for p in team_b]
    else:
        render_pitch(team_a, team_b)
    if len(team_a) == 5 and len(team_b) == 5:
        diff = abs(sum(p["overall"] for p in team_a) - sum(p["overall"] for p in team_b))
        st.subheader("⚖️ Balance Check")
        st.success(f"Difference in team strength: {round(diff,1)} points")
    else:
        st.warning("Assign exactly 5 players to Team A")
