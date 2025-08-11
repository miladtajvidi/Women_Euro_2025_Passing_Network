from statsbombpy import sb
import pandas as pd
import numpy as np
from collections import defaultdict

from mplsoccer import Pitch
from mplsoccer import VerticalPitch
import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
from matplotlib.lines import Line2D


free_comps = sb.competitions()
# print(free_comps)

euro_women_25 = sb.matches(competition_id=53, season_id=315)
# print(euro_women_25.head())


home_team = "England Women's"
away_team = "Spain Women's"
match = euro_women_25[(euro_women_25['home_team'] == home_team)&(euro_women_25['away_team'] == away_team)]

# print(match)
print(match['match_id'].values[0])

events = sb.events(match_id=match['match_id'].values[0])
print(events.columns)

#-----------------------------------------------------------------------------------------------------------

# Step 1: Filter for pass events
pass_events = events[events['type'].apply(lambda x: x['name'] if isinstance(x, dict) else x) == 'Pass']

# Completed passes: where 'pass_outcome' is NaN
completed_passes = pass_events[pass_events['pass_outcome'].isna()]

print(f"Total passes: {len(pass_events)}")
print(f"Completed passes: {len(completed_passes)}")
print(completed_passes[['player', 'team', 'location', 'pass_end_location', 'pass_recipient']].head())

#-----------------------------------------------------------------------------------------------------------

# step 2: Identify Starting XI

# Filter for Starting XI events (usually type is 'Starting XI' or similar)
starting_xi = events[events['type'] == 'Starting XI']

for idx, row in starting_xi.iterrows():
    team = row['team']
    tactics = row['tactics']  # already a dict!
    formation = tactics['formation']
    lineup = tactics['lineup']
    print(f"Team: {team}, Formation: {formation}")
    for player in lineup:
        print(f"  {player['player']['name']} ({player['position']['name']}, #{player['jersey_number']})")

#-----------------------------------------------------------------------------------------------------------

# step 3 :calculating the average positions


# Build a dict of starting XI for each team
starting_xis = {}
for idx, row in starting_xi.iterrows():
    team = row['team']
    lineup = row['tactics']['lineup']
    player_names = [player['player']['name'] for player in lineup]
    starting_xis[team] = player_names

on_ball_types = ['Ball Receipt','Ball Recovery','Dispossessed','Duel','Block','Clearance',
                 'Interception','Carry', 'Dribble', 'Pass', 'Shot','Pressure','Foul Committed',
                 'Foul Won','Goal Keeper','Shield','50/50','Error','Miscontrol','Dribbled Past']

on_ball_events = events[events['type'].apply(lambda x: x['name'] if isinstance(x, dict) else x).isin(on_ball_types)]

# Calculate average position for each starting player using all on-ball events
avg_positions = {}
for team, players in starting_xis.items():
    avg_positions[team] = {}
    for player in players:
        player_events = on_ball_events[(on_ball_events['player'] == player) & (on_ball_events['team'] == team)]
        locations = player_events['location'].dropna().tolist()
        if locations:
            avg_x = np.mean([loc[0] for loc in locations])
            avg_y = np.mean([loc[1] for loc in locations])
            avg_positions[team][player] = (avg_x, avg_y)
        else:
            avg_positions[team][player] = (np.nan, np.nan)

print("Average positions (x, y) for each starting player:")
for team, players in avg_positions.items():
    print(f"\n{team}:")
    for player, pos in players.items():
        print(f"  {player}: {pos}")

#-----------------------------------------------------------------------------------------------------------

# Step 4: Build passing matrix for each team
passing_matrix = {}
for team, players in starting_xis.items():
    # Initialize nested dict for each team
    passing_matrix[team] = defaultdict(int)
    team_passes = completed_passes[completed_passes['team'] == team]
    for _, row in team_passes.iterrows():
        passer = row['player']
        recipient = row['pass_recipient']
        # Only count passes between starting XI players
        if passer in players and recipient in players:
            passing_matrix[team][(passer, recipient)] += 1

# Print passing matrix
print("\nPassing matrix (number of completed passes from A to B):")
for team, matrix in passing_matrix.items():
    print(f"\n{team}:")
    for (passer, recipient), count in matrix.items():
        print(f"  {passer} → {recipient}: {count}")

# Calculate total passes made by each player (as passer)
node_sizes = {}
for team, players in starting_xis.items():
    node_sizes[team] = {}
    for player in players:
        # Count passes made by this player to other starting XI teammates
        node_sizes[team][player] = sum(
            passing_matrix[team][(player, teammate)]
            for teammate in players if (player, teammate) in passing_matrix[team]
        )

#-----------------------------------------------------------------------------------------------------------

# step 5: Visualize average positions and passing matrix

# Scaling factors for node size and edge thickness
NODE_BASE_SIZE = 300
NODE_SCALE = 10
EDGE_BASE_WIDTH = 1
EDGE_SCALE = 0.5


def plot_passing_network(ax, team, avg_positions, passing_matrix, node_sizes):
    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    pitch.draw(ax=ax)
    players = avg_positions[team]
    # Plot nodes (players)
    for player, (x, y) in players.items():
        if not np.isnan(x) and not np.isnan(y):
            size = NODE_BASE_SIZE + node_sizes[team][player] * NODE_SCALE
            ax.scatter(y, x, s=size, color='skyblue', edgecolors='black', zorder=3)
            ax.text(y, x, player.split()[0], ha='center', va='center', fontsize=9, zorder=4)
    # Plot edges (passes)
    for (passer, recipient), count in passing_matrix[team].items():
        x1, y1 = players[passer]
        x2, y2 = players[recipient]
        if not (np.isnan(x1) or np.isnan(y1) or np.isnan(x2) or np.isnan(y2)):
            ax.plot([y1, y2], [x1, x2], color='dodgerblue',
                    linewidth=EDGE_BASE_WIDTH + count * EDGE_SCALE, alpha=0.7, zorder=2)
    ax.set_title(f"{team} Passing Network", fontsize=14)

# Extract match info for titles
match_date = match['match_date'].values[0]
home_score = match['home_score'].values[0]
away_score = match['away_score'].values[0]
result_str = f"{home_team} {home_score} - {away_score} {away_team}"

# Create side-by-side plots for both teams
fig, axes = plt.subplots(1, 2, figsize=(16, 10))

# Main title (top left)
fig.suptitle("Passing Network", fontsize=18, fontweight='bold', x=0.05, ha='left')

# Subplot titles (above each pitch)
axes[0].set_title(f"{home_team}, Starting Eleven", fontsize=14, fontweight='bold', pad=20)
axes[1].set_title(f"{away_team}, Starting Eleven", fontsize=14, fontweight='bold', pad=20)


plot_passing_network(axes[0], f"{home_team}", avg_positions, passing_matrix, node_sizes)
plot_passing_network(axes[1], f"{away_team}", avg_positions, passing_matrix, node_sizes)

# Match info (top right)
fig.text(0.98, 0.96, f"{result_str} {match_date}\nUEFA Women's Euro 2025",
         ha='right', va='top', fontsize=12)

plt.tight_layout(rect=[0, 0, 1, 0.95])  # leave space for suptitle and match info
plt.show()
#-----------------------------------------------------------------------------------------------------------