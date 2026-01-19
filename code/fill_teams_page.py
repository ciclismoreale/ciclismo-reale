import json
import pandas as pd

# Paths to your files
json_file = "data/teams.json"
csv_file = "data/cqranking_riders.csv"
output_file = "squadre.qmd"

# Load teams JSON
with open(json_file, "r", encoding="utf-8") as f:
    teams_data = json.load(f)

# Load riders CSV
df = pd.read_csv(csv_file)
df['Rider'] = df['Rider'].str.strip()  # Strip whitespace from Rider names

# Compute total points for each team
teams_points = []
for team in teams_data["teams"]:
    total_points = 0
    riders_info = []
    for rider_name in team["riders"]:
        rider_row = df[df["Rider"] == rider_name]
        if not rider_row.empty:
            rider_row = rider_row.iloc[0]
            cq = rider_row.get("CQ", 0)
            try:
                cq = float(cq)  # Ensure numeric
            except:
                cq = 0
            flag_html = f'<img src="{rider_row["Country Flag"]}" width="20">' if "Country Flag" in rider_row and pd.notna(rider_row["Country Flag"]) else ""
        else:
            cq = 0
            flag_html = ""
        total_points += cq
        riders_info.append((flag_html, rider_name, int(cq)))  # Convert rider points to integer
    teams_points.append({
        "name": team["name"],
        "total_points": int(total_points),  # Convert team total to integer
        "riders_info": riders_info
    })

# Sort teams by total points descending
teams_points.sort(key=lambda x: x["total_points"], reverse=True)

# Medal emojis for top 4
medals = ["🥇", "🥈", "🥉", "🪵"]

quarto_content = ""

for idx, team in enumerate(teams_points, start=1):
    # Determine label: medal emoji or number
    label = medals[idx - 1] if idx <= 4 else f"{idx}."
    
    # Team header with points aligned right
    quarto_content += f"### {label} {team['name']} <span style='float:right'>{team['total_points']}</span>\n\n"

    # Collapsible section for riders
    quarto_content += "<details>\n<summary>Corridori</summary>\n\n"
    quarto_content += '<table style="border-collapse: collapse; width:100%;">\n'
    quarto_content += '<thead>\n<tr>\n'
    headers = ["", "", "CQ pts"]
    widths = ["40px", "220px", "50px"]
    for h, w in zip(headers, widths):
        quarto_content += f'<th style="padding:4px;width:{w};text-align:center;">{h}</th>\n'
    quarto_content += '</tr>\n</thead>\n<tbody>\n'

    for flag_html, name, cq in team["riders_info"]:
        quarto_content += (
            f'<tr>\n'
            f'<td style="text-align:center;">{flag_html}</td>\n'
            f'<td style="text-align:left;">{name}</td>\n'
            f'<td style="text-align:center;">{cq}</td>\n'
            '</tr>\n'
        )

    quarto_content += '</tbody>\n</table>\n\n</details>\n\n'

# Write Quarto file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("""---
title: "Classifiche"
---

""")
    f.write(quarto_content)

print(f"Quarto file with team rankings written to {output_file}")

