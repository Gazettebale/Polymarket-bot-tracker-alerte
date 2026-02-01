"""
Script pour voir les statistiques des alertes Polymarket
"""

import csv
import os
from datetime import datetime
from collections import Counter

def view_stats():
    """Affiche les statistiques des alertes"""
    
    csv_file = 'polymarket_alerts_log.csv'
    
    if not os.path.exists(csv_file):
        print("❌ Aucun fichier de log trouvé!")
        print("📝 Lance le bot d'abord pour générer des alertes.")
        return
    
    # Lit le fichier CSV
    alerts = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        alerts = list(reader)
    
    if not alerts:
        print("📊 Aucune alerte enregistrée pour le moment.")
        return
    
    print("="*80)
    print("📊 STATISTIQUES DES ALERTES POLYMARKET")
    print("="*80)
    
    # Stats globales
    print(f"\n📈 NOMBRE TOTAL D'ALERTES: {len(alerts)}")
    
    # Par type d'alerte
    alert_types = Counter([a['Alert_Type'] for a in alerts])
    print(f"\n🎯 PAR TYPE D'ALERTE:")
    for alert_type, count in alert_types.most_common():
        print(f"   {alert_type}: {count} alertes")
    
    # Avec whale activity
    whale_alerts = sum(1 for a in alerts if a.get('Whale_Activity') == 'YES')
    print(f"\n🐋 WHALE ACTIVITY DÉTECTÉE: {whale_alerts} fois ({whale_alerts/len(alerts)*100:.1f}%)")
    
    # Meilleurs scores
    scored_alerts = [a for a in alerts if a.get('Trader_Score') and int(a.get('Trader_Score', 0)) > 0]
    if scored_alerts:
        avg_score = sum(int(a['Trader_Score']) for a in scored_alerts) / len(scored_alerts)
        max_score = max(int(a['Trader_Score']) for a in scored_alerts)
        print(f"\n⭐ SCORES:")
        print(f"   Score moyen: {avg_score:.1f}/10")
        print(f"   Score max: {max_score}/10")
    
    # Top marchés
    markets = Counter([a['Market_Question'][:50] + "..." for a in alerts])
    print(f"\n🔥 TOP 5 MARCHÉS LES PLUS ALERTÉS:")
    for market, count in markets.most_common(5):
        print(f"   • {market} ({count}x)")
    
    # Dernières alertes
    print(f"\n📝 DERNIÈRES 5 ALERTES:")
    for alert in alerts[-5:]:
        print(f"\n   [{alert.get('Timestamp', 'N/A')}] {alert.get('Alert_Type', 'N/A')}")
        print(f"   📊 {alert.get('Market_Question', 'N/A')[:60]}...")
        print(f"   ✅ {alert.get('Outcome', 'N/A')} @ {alert.get('Probability', 'N/A')}")
        print(f"   💰 Gain potentiel: {alert.get('Potential_Gain_Percent', 'N/A')}")
    
    print("\n" + "="*80)
    print(f"📁 Fichier complet: {csv_file}")
    print("="*80)

if __name__ == "__main__":
    view_stats()
