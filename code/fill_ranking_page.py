import pandas as pd
import math

# File paths
csv_file = "data/cqranking_riders.csv"
output_file = "cq_ranking.qmd"

# Read CSV
df = pd.read_csv(csv_file)

ROWS_PER_PAGE = 50
num_pages = math.ceil(len(df) / ROWS_PER_PAGE)

# Open file to write
with open(output_file, "w", encoding="utf-8") as f:

    # ---- Quarto title ----
    f.write("""---
title: "CQ Ranking"
---

""")

    # ---- Table ----
    f.write('<table style="border-collapse: collapse; width:100%;">\n')
    f.write('<thead>\n<tr>\n')

    headers = ["Rank", "", "", "", "", "CQ pts"]
    widths = ["30px", "30px", "200px", "120px", "80px", "50px"]

    for h, w in zip(headers, widths):
        f.write(f'<th style="padding:4px;width:{w};text-align:center;">{h}</th>\n')

    f.write('</tr>\n</thead>\n<tbody>\n')

    # ---- Table rows ----
    for i, row in df.iterrows():
        page = i // ROWS_PER_PAGE
        flag = f'<img src="{row["Country Flag"]}" width="20">' if pd.notna(row["Country Flag"]) else ""
        rider = row["Rider"].replace("  ", "&nbsp;&nbsp;") if pd.notna(row["Rider"]) else ""
        team = row["Team"] if pd.notna(row["Team"]) else ""
        dob = row["Date of birth"] if pd.notna(row["Date of birth"]) else ""

        f.write(
            f'<tr class="page page-{page}" style="display:none;">\n'
            f'<td style="text-align:center;">{row["Rank"]}</td>\n'
            f'<td style="text-align:center;">{flag}</td>\n'
            f'<td style="text-align:left;">{rider}</td>\n'
            f'<td style="text-align:center;">{team}</td>\n'
            f'<td style="text-align:center;">{dob}</td>\n'
            f'<td style="text-align:center;">{row["CQ"]}</td>\n'
            '</tr>\n'
        )

    f.write('</tbody>\n</table>\n')

    # ---- Pagination buttons (bottom, centered) ----
    f.write("""
<div id="pagination" style="margin-top:15px; text-align:center;">
""")

    for i in range(num_pages):
        f.write(
            f'<button onclick="showPage({i})" '
            f'style="margin:3px;padding:5px 10px;">{i+1}</button>\n'
        )

    f.write('</div>\n')

    # ---- JavaScript pagination ----
    f.write("""
<script>
function showPage(page) {
    document.querySelectorAll('.page').forEach(row => {
        row.style.display = 'none';
    });
    document.querySelectorAll('.page-' + page).forEach(row => {
        row.style.display = '';
    });

    document.querySelectorAll('#pagination button').forEach((b,i) => {
        b.style.fontWeight = (i === page) ? 'bold' : 'normal';
    });
}
showPage(0);
</script>
""")

print(f"Paginated table written to '{output_file}'")
