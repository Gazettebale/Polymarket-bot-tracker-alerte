"""
Script pour voir les stats des notifications envoyées
Utile pour tracker tes opportunités et performances
"""

import sqlite3
from datetime import datetime, timedelta
import os

def get_stats():
    """Affiche les statistiques des notifications"""
    
    if not os.path.exists('polymarket_alerts.db'):
        print("❌ Aucune base de données trouvée")
        print("💡 Lance le bot au moins une fois pour créer la base")
        return
    
    conn = sqlite3.connect('polymarket_alerts.db')
    cursor = conn.cursor()
    
    print("="*80)
    print("📊 STATISTIQUES DU BOT POLYMARKET")
    print("="*80)
    
    # Total notifications
    cursor.execute("SELECT COUNT(*) FROM notified_markets")
    total = cursor.fetchone()[0]
    print(f"\n📬 Total notifications envoyées: {total}")
    
    if total == 0:
        print("\n💡 Aucune notification encore. Le bot cherche des opportunités...")
        conn.close()
        return
    
    # Dernières 24h
    cursor.execute("""
        SELECT COUNT(*) FROM notified_markets 
        WHERE datetime(notified_at) > datetime('now', '-24 hours')
    """)
    last_24h = cursor.fetchone()[0]
    print(f"📅 Dernières 24h: {last_24h} notifications")
    
    # Dernières 7 jours
    cursor.execute("""
        SELECT COUNT(*) FROM notified_markets 
        WHERE datetime(notified_at) > datetime('now', '-7 days')
    """)
    last_7d = cursor.fetchone()[0]
    print(f"📅 Derniers 7 jours: {last_7d} notifications")
    
    # Probabilité moyenne
    cursor.execute("SELECT AVG(probability) FROM notified_markets")
    avg_prob = cursor.fetchone()[0]
    if avg_prob:
        print(f"\n📈 Probabilité moyenne: {avg_prob*100:.2f}%")
    
    # Top marchés
    print("\n" + "="*80)
    print("🔥 TOP 10 DERNIÈRES OPPORTUNITÉS")
    print("="*80)
    
    cursor.execute("""
        SELECT market_slug, outcome, probability, notified_at
        FROM notified_markets
        ORDER BY notified_at DESC
        LIMIT 10
    """)
    
    for i, row in enumerate(cursor.fetchall(), 1):
        slug, outcome, prob, timestamp = row
        
        # Parse timestamp
        try:
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        except:
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        
        time_ago = datetime.now() - dt
        if time_ago.days > 0:
            time_str = f"il y a {time_ago.days}j"
        elif time_ago.seconds > 3600:
            time_str = f"il y a {time_ago.seconds//3600}h"
        else:
            time_str = f"il y a {time_ago.seconds//60}min"
        
        print(f"\n#{i} - {time_str}")
        print(f"   Outcome: {outcome}")
        print(f"   Probabilité: {prob*100:.2f}%")
        print(f"   Slug: {slug}")
    
    # Distribution par outcome
    print("\n" + "="*80)
    print("📊 DISTRIBUTION YES/NO")
    print("="*80)
    
    cursor.execute("""
        SELECT outcome, COUNT(*) 
        FROM notified_markets 
        GROUP BY outcome
    """)
    
    for outcome, count in cursor.fetchall():
        pct = (count / total * 100) if total > 0 else 0
        print(f"{outcome}: {count} ({pct:.1f}%)")
    
    conn.close()
    
    print("\n" + "="*80)
    print("✅ Fin des stats")
    print("="*80)

if __name__ == "__main__":
    get_stats()
