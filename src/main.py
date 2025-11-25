
import pandas as pd
from portfolio import Portfolio
from pathlib import Path
import plotly.express as px

# Charger les données
positions = pd.read_csv("data/Classeur5.csv", sep=";")
positions.columns = [col.strip() for col in positions.columns]

# Créer le portefeuille
portfolio = Portfolio(positions)

print("Téléchargement des prix actuels...")
portfolio.load_current_prices()

# Calculer la performance
performance_df = portfolio.calculate_performance()
print(performance_df)

# Sauvegarder en CSV et JSON
output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)
performance_df.to_csv(output_dir / "portfolio_performance_live.csv", index=False)
performance_df.to_json(output_dir / "portfolio_performance_live.json", orient="records", indent=4)

# Graphique ROI par actif
fig_roi = px.bar(performance_df, x="Ticker", y="ROI %", color="Ticker", title="ROI par actif")

# Affichage interactif (dans Codespaces ou navigateur)
fig_roi.show()

# Export HTML (au lieu de PNG)
fig_roi.write_html(str(output_dir / "roi_per_asset.html"))

print(f"✅ Fichiers générés dans {output_dir}")