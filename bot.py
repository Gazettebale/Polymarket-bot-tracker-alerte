#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ██████╗  ██████╗ ██╗  ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ██╗  ██╗      ║
║     ██╔══██╗██╔═══██╗██║  ╚██╗ ██╔╝████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝      ║
║     ██████╔╝██║   ██║██║   ╚████╔╝ ██╔████╔██║███████║██████╔╝█████╔╝       ║
║     ██╔═══╝ ██║   ██║██║    ╚██╔╝  ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗       ║
║     ██║     ╚██████╔╝███████╗██║   ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗      ║
║     ╚═╝      ╚═════╝ ╚══════╝╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝      ║
║                                                                              ║
║                    🏆 POLYMARKET WHALE TRACKER 🏆                            ║
║                                                                              ║
║     🟢 SAFE BETS (90-98.5% | <20 days | $80K+ liquidity)                    ║
║     🔵 VOLUME FARMING (98.5-99.5% | <4 days)                                ║
║     🐋 WHALE CONSENSUS: 5+ whales OR 1 whale 80%+ WR                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Set
from collections import defaultdict
import logging

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use os.environ directly

# ═══════════════════════════════════════════════════════════════════════════════
# 🐋 TOP TRADERS DATABASE - 42 WHALES
# ═══════════════════════════════════════════════════════════════════════════════

TOP_TRADERS = {
    # 👑 LEGENDARY (95%+ WR)
    "0x4638d71d7b2d36eb590b5e1824955712dc8ad587": {"name": "jeb2016", "win_rate": 100.0, "rank": 1590, "tier": "LEGENDARY"},
    "0x9b979a065641e8cfde3022a30ed2d9415cf55e12": {"name": "LlamaEnjoyer", "win_rate": 96.0, "rank": 69, "tier": "LEGENDARY"},
    "0x7f3c8979d0afa00007bae4747d5347122af05613": {"name": "LucasMeow", "win_rate": 95.5, "rank": 411, "tier": "LEGENDARY"},
    
    # 🏆 ELITE (85-95% WR)
    "0x2e0b70d482e6b389e81dea528be57d825dd48070": {"name": "Trump2028", "win_rate": 92.2, "rank": 447, "tier": "ELITE"},
    "0x6ffb4354cbe6e0f9989e3b55564ec5fb8646a834": {"name": "AgricultureSecretary", "win_rate": 91.7, "rank": 221, "tier": "ELITE"},
    "0xa9b44dca52ed35e59ac2a6f49d1203b8155464ed": {"name": "VvVv", "win_rate": 90.4, "rank": 375, "tier": "ELITE"},
    "0x8861f0bb5e0c19474ba73beeadc13ed8915beed6": {"name": "yjcr", "win_rate": 89.7, "rank": 60, "tier": "ELITE"},
    "0xfc25f141ed27bb1787338d2c4e7f51e3a15e1f7f": {"name": "kutar", "win_rate": 88.8, "rank": 274, "tier": "ELITE"},
    "0xed107a85a4585a381e48c7f7ca4144909e7dd2e5": {"name": "bobe2", "win_rate": 87.0, "rank": 52, "tier": "ELITE"},
    "0x000d257d2dc7616feaef4ae0f14600fdf50a758e": {"name": "scottilicious", "win_rate": 84.9, "rank": 44, "tier": "ELITE"},
    
    # 🥇 TOP (80-85% WR)
    "0xcd71fd5370880f3d92bb941e628c05840fe0d127": {"name": "Kevindoto", "win_rate": 81.5, "rank": 480, "tier": "TOP"},
    
    # 🥈 HIGH (70-80% WR)
    "0xa4b366ad22fc0d06f1e934ff468e8922431a87b8": {"name": "HolyMoses7", "win_rate": 78.6, "rank": 789, "tier": "HIGH"},
    "0x6bab41a0dc40d6dd4c1a915b8c01969479fd1292": {"name": "Dropper", "win_rate": 78.4, "rank": 95, "tier": "HIGH"},
    "0x220ce36c47fa467152b3bd8d431af74f232243c8": {"name": "numbersandletters", "win_rate": 75.9, "rank": 384, "tier": "HIGH"},
    "0xd218e474776403a330142299f7796e8ba32eb5c9": {"name": "BigVolume_d218", "win_rate": 73.5, "rank": 107, "tier": "HIGH"},
    "0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1": {"name": "aenews2", "win_rate": 72.9, "rank": 22, "tier": "HIGH"},
    "0x53d2d3c78597a78402d4db455a680da7ef560c3f": {"name": "abeautifulmind", "win_rate": 72.5, "rank": 64, "tier": "HIGH"},
    "0x83a296505eb520c9d35823571204ced41fd69452": {"name": "0x83a2_whale", "win_rate": 72.2, "rank": 1543, "tier": "HIGH"},
    
    # 🥉 SOLID (60-70% WR)
    "0x7c3db723f1d4d8cb9c550095203b686cb11e5c6b": {"name": "Car", "win_rate": 69.2, "rank": 106, "tier": "SOLID"},
    "0x5bffcf561bcae83af680ad600cb99f1184d6ffbe": {"name": "YatSen", "win_rate": 69.2, "rank": 19, "tier": "SOLID"},
    "0xe3726a1b9c6ba2f06585d1c9e01d00afaedaeb38": {"name": "MegaVolume_e372", "win_rate": 69.1, "rank": 324, "tier": "SOLID"},
    "0xee00ba338c59557141789b127927a55f5cc5cea1": {"name": "S-Works", "win_rate": 67.3, "rank": 24, "tier": "SOLID"},
    "0x6770bf688b8121331b1c5cfd7723ebd4152545fb": {"name": "GreekGamblerPM", "win_rate": 65.6, "rank": 4834, "tier": "SOLID"},
    "0x24c8cf69a0e0a17eee21f69d29752bfa32e823e1": {"name": "debased", "win_rate": 65.1, "rank": 46, "tier": "SOLID"},
    "0x4b92a2d2fd3807981a5dddae7315122530a542e6": {"name": "wisser", "win_rate": 65.0, "rank": 406, "tier": "SOLID"},
    "0x7ac83882979ccb5665cea83cb269e558b55077cd": {"name": "nicoco89", "win_rate": 64.7, "rank": 1267, "tier": "SOLID"},
    "0xd1acd3925d895de9aec98ff95f3a30c5279d08d5": {"name": "Kickstand7", "win_rate": 64.6, "rank": 45, "tier": "SOLID"},
    "0x551e72eda42a5ab39d6d78239a1d9bbb5db6b0e0": {"name": "GayPride", "win_rate": 64.3, "rank": 107, "tier": "SOLID"},
    "0xdbade4c82fb72780a0db9a38f821d8671aba9c95": {"name": "SwissMiss", "win_rate": 64.0, "rank": 16, "tier": "SOLID"},
    "0x9d84ce0306f8551e02efef1680475fc0f1dc1344": {"name": "Domer", "win_rate": 63.4, "rank": 19, "tier": "SOLID"},
    "0xf2f6af4f27ec2dcf4072095ab804016e14cd5817": {"name": "gopfan2", "win_rate": 63.0, "rank": 51, "tier": "SOLID"},
    "0x509587cbb541251c74f261df3421f1fcc9fdc97c": {"name": "BuckMySalls", "win_rate": 62.7, "rank": 67, "tier": "SOLID"},
    "0x0f37cb80dee49d55b5f6d9e595d52591d6371410": {"name": "Hans323", "win_rate": 61.7, "rank": 904, "tier": "SOLID"},
    "0x06ecb7e739f5455922ce57e83284f132c7f0f845": {"name": "frosen", "win_rate": 60.8, "rank": 434, "tier": "SOLID"},
    
    # 📊 VOLUME (High volume traders)
    "0xb74711992caf6d04fa55eecc46b8efc95311b050": {"name": "Kapii", "win_rate": 59.5, "rank": 63, "tier": "VOLUME"},
    "0x629bc4a1e53e1d475beb7ea3d388791e96dd995a": {"name": "lava-lava", "win_rate": 58.9, "rank": 172, "tier": "VOLUME"},
    "0x55be7aa03ecfbe37aa5460db791205f7ac9ddca3": {"name": "coinman2", "win_rate": 57.3, "rank": 53, "tier": "VOLUME"},
    "0x8795bcb2fe129d1ea3e3d73bc13a3d8078047544": {"name": "ciro2", "win_rate": 57.2, "rank": 93, "tier": "VOLUME"},
    "0x39932ca2b7a1b8ab6cbf0b8f7419261b950ccded": {"name": "kIjsa12345", "win_rate": 53.8, "rank": 255, "tier": "VOLUME"},
    "0x889e7f0464c72eb8cda1525ebc12b6aaba9d09e0": {"name": "Punchbowl", "win_rate": 53.6, "rank": 90, "tier": "VOLUME"},
    "0x31519628fb5e5aa559d4ba27aa1248810b9f0977": {"name": "qwertyasdfghjkl", "win_rate": 53.3, "rank": 35, "tier": "VOLUME"},
    "0x75e765216a57942d738d880ffcda854d9f869080": {"name": "25usdc", "win_rate": 48.0, "rank": 1037, "tier": "VOLUME"},
}

# Create lowercase lookup set for matching
TRACKED_ADDRESSES = {addr.lower() for addr in TOP_TRADERS.keys()}

# ═══════════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION - Load from environment variables
# ═══════════════════════════════════════════════════════════════════════════════

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Validate credentials
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ ERROR: Missing Telegram credentials!")
    print("Please create a .env file with:")
    print("  TELEGRAM_BOT_TOKEN=your_token")
    print("  TELEGRAM_CHAT_ID=your_chat_id")
    print("\nSee .env.example for template")
    exit(1)

GAMMA_API_BASE = "https://gamma-api.polymarket.com"
DATA_API_BASE = "https://data-api.polymarket.com"

INVESTMENT_AMOUNT = int(os.getenv("INVESTMENT_AMOUNT", "500"))

# ═══════════════════════════════════════════════════════════════════════════════
# 🟢 SAFE BETS CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

SAFE_ENABLED = True
SAFE_MIN_PROBABILITY = 0.90
SAFE_MAX_PROBABILITY = 0.985
SAFE_MIN_LIQUIDITY = 80000
SAFE_MIN_VOLUME = 10000
SAFE_MAX_DAYS_TO_RESOLUTION = 20

# ═══════════════════════════════════════════════════════════════════════════════
# 🔵 VOLUME FARMING CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

FARMING_ENABLED = True
FARMING_MIN_PROBABILITY = 0.985
FARMING_MAX_PROBABILITY = 0.995
FARMING_MIN_LIQUIDITY = 65000
FARMING_MIN_VOLUME = 10000
FARMING_MAX_DAYS_TO_RESOLUTION = 4

# ═══════════════════════════════════════════════════════════════════════════════
# 🐋 WHALE CONSENSUS CONFIG (CONSERVATIVE)
# ═══════════════════════════════════════════════════════════════════════════════

WHALE_CONSENSUS_ENABLED = True
WHALE_MIN_CONSENSUS = 5           # Minimum 5 whales on same market/direction
WHALE_ELITE_MIN_WINRATE = 80.0    # Min win rate for solo alert
WHALE_MIN_TOTAL_SIZE = 1000       # Minimum $1000 total bet
WHALE_MIN_INDIVIDUAL_SIZE = 50    # Minimum $50 per individual trade
WHALE_CONSENSUS_WINDOW_HOURS = 24 # 24h window for consensus
WHALE_TRADES_FETCH_LIMIT = 1000   # Number of trades to fetch

# ═══════════════════════════════════════════════════════════════════════════════
# ⚙️ SYSTEM CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

SCAN_INTERVAL_SECONDS = int(os.getenv("SCAN_INTERVAL", "120"))
MAX_MARKETS_PER_REQUEST = 100

# State tracking
sent_alerts: Set[str] = set()
sent_consensus_alerts: Set[str] = set()
processed_trade_hashes: Set[str] = set()

# Whale positions tracking: {market_slug: {outcome: [{whale_info}, ...]}}
whale_positions: Dict[str, Dict[str, List[Dict]]] = defaultdict(lambda: defaultdict(list))
whale_positions_timestamps: Dict[str, datetime] = {}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 📱 TELEGRAM FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def send_telegram(message: str) -> bool:
    """Send message to Telegram"""
    try:
        import urllib3
        urllib3.disable_warnings()
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        response = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }, timeout=30, verify=False)
        if response.status_code == 200:
            logger.info("✅ Telegram message sent")
            return True
        else:
            logger.warning(f"Telegram returned: {response.status_code}")
            return False
    except Exception as e:
        logger.warning(f"Telegram error: {e}")
        return False


def calculate_profit(probability: float, investment: float = INVESTMENT_AMOUNT) -> float:
    """Calculate potential profit on investment"""
    shares = investment / probability
    payout = shares * 1.0
    profit = payout - investment
    return profit


# ═══════════════════════════════════════════════════════════════════════════════
# 🟢 SAFE BET ALERTS
# ═══════════════════════════════════════════════════════════════════════════════

def alert_safe_bet(market: Dict, probability: float, outcome: str, days: int):
    """Send SAFE BET alert"""
    if not SAFE_ENABLED:
        return
    
    alert_id = f"SAFE_{market.get('id', '')}_{outcome}"
    if alert_id in sent_alerts:
        return
    
    question = market.get('question', 'Unknown Market')
    liquidity = float(market.get('liquidity', 0))
    volume = float(market.get('volume', 0))
    
    slug = market.get('slug', '')
    url = f"https://polymarket.com/event/{slug}" if slug else "https://polymarket.com"
    
    profit = calculate_profit(probability, INVESTMENT_AMOUNT)
    roi_pct = (profit / INVESTMENT_AMOUNT) * 100
    
    message = f"""🟢 <b>SAFE BET OPPORTUNITY</b> 🟢

📊 {question}

━━━━━━━━━━━━━━━━━━━━━━

🎯 Bet: <b>{outcome}</b>
📈 Probability: <b>{probability*100:.1f}%</b>
⏰ Resolution: {days} day{'s' if days > 1 else ''}

━━━━━━━━━━━━━━━━━━━━━━

💰 With ${INVESTMENT_AMOUNT}:
   Potential profit: <b>${profit:.2f}</b> (+{roi_pct:.1f}%)

💧 Liquidity: ${liquidity:,.0f}
📊 Volume: ${volume:,.0f}

🔗 {url}"""
    
    if send_telegram(message):
        sent_alerts.add(alert_id)


# ═══════════════════════════════════════════════════════════════════════════════
# 🔵 VOLUME FARMING ALERTS
# ═══════════════════════════════════════════════════════════════════════════════

def alert_farming(market: Dict, probability: float, outcome: str, days: int):
    """Send VOLUME FARMING alert"""
    if not FARMING_ENABLED:
        return
    
    alert_id = f"FARM_{market.get('id', '')}_{outcome}"
    if alert_id in sent_alerts:
        return
    
    question = market.get('question', 'Unknown Market')
    liquidity = float(market.get('liquidity', 0))
    volume = float(market.get('volume', 0))
    
    slug = market.get('slug', '')
    url = f"https://polymarket.com/event/{slug}" if slug else "https://polymarket.com"
    
    profit = calculate_profit(probability, INVESTMENT_AMOUNT)
    roi_pct = (profit / INVESTMENT_AMOUNT) * 100
    
    message = f"""🔵 <b>VOLUME FARMING</b> 🔵

📊 {question}

━━━━━━━━━━━━━━━━━━━━━━

🎯 Bet: <b>{outcome}</b>
📈 Probability: <b>{probability*100:.2f}%</b>
⏰ Resolution: {days} day{'s' if days > 1 else ''}

━━━━━━━━━━━━━━━━━━━━━━

💰 With ${INVESTMENT_AMOUNT}:
   Potential profit: <b>${profit:.2f}</b> (+{roi_pct:.1f}%)

💧 Liquidity: ${liquidity:,.0f}

🔗 {url}"""
    
    if send_telegram(message):
        sent_alerts.add(alert_id)


# ═══════════════════════════════════════════════════════════════════════════════
# 🐋 WHALE ALERTS
# ═══════════════════════════════════════════════════════════════════════════════

def alert_elite_whale(trader: Dict, trade: Dict, market_question: str, market_url: str):
    """Send ELITE WHALE alert (80%+ win rate trader)"""
    alert_id = f"ELITE_{trader.get('name', '')}_{trade.get('market_slug', '')}_{trade.get('outcome', '')}"
    if alert_id in sent_consensus_alerts:
        return
    
    tier_emoji = {
        "LEGENDARY": "👑", 
        "ELITE": "🏆", 
        "TOP": "🥇"
    }.get(trader.get("tier", ""), "🐋")
    
    side_emoji = "🟢 BUY" if trade.get('side', '').upper() == "BUY" else "🔴 SELL"
    
    message = f"""{tier_emoji} <b>ELITE WHALE ALERT</b> {tier_emoji}

━━━━━━━━━━━━━━━━━━━━━━

👤 <b>{trader.get('name', 'Unknown')}</b>
   Tier: {trader.get('tier', 'Unknown')}
   Win Rate: <b>{trader.get('win_rate', 0)}%</b>
   Rank: #{trader.get('rank', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━

{side_emoji} <b>{trade.get('outcome', 'Unknown')}</b>
💵 Size: ${trade.get('size', 0):,.2f}
📈 Price: {trade.get('price', 0)*100:.1f}%

━━━━━━━━━━━━━━━━━━━━━━

📊 {market_question[:80]}{'...' if len(market_question) > 80 else ''}

🔗 {market_url}"""
    
    if send_telegram(message):
        sent_consensus_alerts.add(alert_id)
        logger.info(f"👑 Elite whale alert: {trader.get('name')} on {trade.get('outcome')}")


def alert_whale_consensus(market_slug: str, outcome: str, whales: List[Dict], market_question: str):
    """Send WHALE CONSENSUS alert (5+ whales on same direction)"""
    alert_id = f"CONSENSUS_{market_slug}_{outcome}"
    if alert_id in sent_consensus_alerts:
        return
    
    total_size = sum(w.get('size', 0) for w in whales)
    if total_size < WHALE_MIN_TOTAL_SIZE:
        return
    
    avg_winrate = sum(w.get('win_rate', 0) for w in whales) / len(whales)
    
    whale_list = "\n".join([
        f"   • {w.get('name', 'Unknown')} ({w.get('win_rate', 0)}% WR) - ${w.get('size', 0):,.0f}"
        for w in sorted(whales, key=lambda x: x.get('win_rate', 0), reverse=True)[:5]
    ])
    
    market_url = f"https://polymarket.com/event/{market_slug}"
    
    message = f"""🐋🐋🐋 <b>WHALE CONSENSUS</b> 🐋🐋🐋

━━━━━━━━━━━━━━━━━━━━━━

📊 {market_question[:80]}{'...' if len(market_question) > 80 else ''}

🎯 Direction: <b>{outcome}</b>
👥 Whales: <b>{len(whales)}</b>
💰 Total bet: <b>${total_size:,.0f}</b>
📈 Avg Win Rate: <b>{avg_winrate:.1f}%</b>

━━━━━━━━━━━━━━━━━━━━━━

🐋 Top Whales:
{whale_list}

🔗 {market_url}"""
    
    if send_telegram(message):
        sent_consensus_alerts.add(alert_id)
        logger.info(f"🐋 Consensus alert: {len(whales)} whales on {outcome}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🌐 API FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_markets(limit: int = 100, offset: int = 0) -> List[Dict]:
    """Fetch markets from Gamma API"""
    try:
        response = requests.get(
            f"{GAMMA_API_BASE}/markets",
            params={"limit": limit, "offset": offset, "active": "true", "closed": "false"},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"API error: {e}")
        return []


def fetch_market_by_slug(slug: str) -> Optional[Dict]:
    """Fetch single market by slug"""
    try:
        response = requests.get(
            f"{GAMMA_API_BASE}/markets",
            params={"slug": slug},
            timeout=30
        )
        if response.status_code == 200:
            markets = response.json()
            return markets[0] if markets else None
        return None
    except:
        return None


def parse_prices(market: Dict) -> Dict:
    """Parse market prices from Gamma API format"""
    result = {"outcomes": [], "prices": [], "ok": False}
    try:
        outcomes_raw = market.get("outcomes", "[]")
        outcomes = json.loads(outcomes_raw) if isinstance(outcomes_raw, str) else outcomes_raw
        result["outcomes"] = outcomes
        
        prices_raw = market.get("outcomePrices", "[]")
        prices = json.loads(prices_raw) if isinstance(prices_raw, str) else prices_raw
        result["prices"] = [float(p) for p in prices] if prices else []
        result["ok"] = len(result["prices"]) > 0
    except:
        pass
    return result


def get_days_to_resolution(market: Dict) -> Optional[int]:
    """Calculate days until market resolution"""
    end_date_str = market.get("endDate")
    if not end_date_str:
        return None
    try:
        end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
        now = datetime.now(end_date.tzinfo) if end_date.tzinfo else datetime.now()
        days = (end_date - now).days
        return max(0, days)
    except:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 MARKET ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_market(market: Dict) -> Dict:
    """Analyze a market for opportunities"""
    result = {"safe": [], "farming": []}
    
    if market.get("closed") or not market.get("active", True):
        return result
    
    liquidity = float(market.get("liquidity", 0))
    volume = float(market.get("volume", 0))
    days = get_days_to_resolution(market)
    
    parsed = parse_prices(market)
    if not parsed["ok"]:
        return result
    
    outcomes = parsed["outcomes"]
    prices = parsed["prices"]
    
    # Check if this is a simple Yes/No market
    is_yes_no_market = (
        len(outcomes) == 2 and 
        outcomes[0].lower() in ["yes", "no"] and 
        outcomes[1].lower() in ["yes", "no"]
    )
    
    for outcome, price in zip(outcomes, prices):
        # Skip "No" outcomes on multi-option markets
        if not is_yes_no_market and outcome.lower() == "no":
            continue
        
        # 🟢 SAFE BET CHECK
        if (SAFE_ENABLED and
            SAFE_MIN_PROBABILITY <= price <= SAFE_MAX_PROBABILITY and
            liquidity >= SAFE_MIN_LIQUIDITY and
            volume >= SAFE_MIN_VOLUME and
            days is not None and days <= SAFE_MAX_DAYS_TO_RESOLUTION):
            
            result["safe"].append({
                "outcome": outcome,
                "probability": price,
                "days": days,
                "market": market
            })
        
        # 🔵 FARMING CHECK
        if (FARMING_ENABLED and
            FARMING_MIN_PROBABILITY <= price <= FARMING_MAX_PROBABILITY and
            liquidity >= FARMING_MIN_LIQUIDITY and
            volume >= FARMING_MIN_VOLUME and
            days is not None and days <= FARMING_MAX_DAYS_TO_RESOLUTION):
            
            result["farming"].append({
                "outcome": outcome,
                "probability": price,
                "days": days,
                "market": market
            })
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# 🐋 WHALE TRACKING
# ═══════════════════════════════════════════════════════════════════════════════

def add_whale_position(market_slug: str, outcome: str, whale_data: Dict) -> bool:
    """Add whale position to tracking, returns True if new"""
    # Check for duplicate
    existing = whale_positions[market_slug][outcome]
    for w in existing:
        if w.get('address') == whale_data.get('address'):
            return False
    
    whale_positions[market_slug][outcome].append(whale_data)
    whale_positions_timestamps[market_slug] = datetime.now()
    return True


def cleanup_old_positions():
    """Remove positions older than consensus window"""
    cutoff = datetime.now() - timedelta(hours=WHALE_CONSENSUS_WINDOW_HOURS)
    
    markets_to_remove = []
    for market_slug, timestamp in whale_positions_timestamps.items():
        if timestamp < cutoff:
            markets_to_remove.append(market_slug)
    
    for market_slug in markets_to_remove:
        del whale_positions[market_slug]
        del whale_positions_timestamps[market_slug]
    
    if markets_to_remove:
        logger.info(f"Cleaned up {len(markets_to_remove)} old market positions")


def check_consensus_alerts():
    """Check for whale consensus and send alerts"""
    if not WHALE_CONSENSUS_ENABLED:
        return
    
    cleanup_old_positions()
    
    for market_slug, outcomes in whale_positions.items():
        for outcome, whales in outcomes.items():
            if len(whales) >= WHALE_MIN_CONSENSUS:
                market_question = whales[0].get('market_question', 'Unknown Market') if whales else 'Unknown'
                alert_whale_consensus(market_slug, outcome, whales, market_question)


def check_whale_trades():
    """Check for whale trades using Data API"""
    if not WHALE_CONSENSUS_ENABLED:
        return
    
    logger.info("🐋 Checking whale trades...")
    
    new_whale_trades = 0
    elite_alerts = 0
    
    try:
        # Fetch recent trades from Data API
        response = requests.get(
            f"{DATA_API_BASE}/trades",
            params={"limit": WHALE_TRADES_FETCH_LIMIT},
            timeout=30,
            verify=False
        )
        
        if response.status_code != 200:
            logger.warning(f"Data API returned {response.status_code}")
            return
        
        trades = response.json()
        if not isinstance(trades, list):
            trades = trades.get('trades', [])
        
        logger.info(f"📊 Fetched {len(trades)} trades from Data API")
        
    except Exception as e:
        logger.error(f"Failed to fetch trades: {e}")
        return
    
    for trade in trades:
        # Create unique hash for this trade
        trade_hash = f"{trade.get('id', '')}_{trade.get('timestamp', '')}_{trade.get('maker', '')}"
        
        if trade_hash in processed_trade_hashes:
            continue
        processed_trade_hashes.add(trade_hash)
        
        # Check if maker or taker is a tracked whale
        addresses_to_check = [
            trade.get("maker", "").lower(),
            trade.get("taker", "").lower(),
            trade.get("owner", "").lower(),
            trade.get("user", "").lower(),
        ]
        
        whale_address = None
        for addr in addresses_to_check:
            if addr and addr in TRACKED_ADDRESSES:
                whale_address = addr
                break
        
        if not whale_address:
            continue
        
        trader_info = TOP_TRADERS.get(whale_address, {})
        
        # Parse trade data
        size = float(trade.get('size', 0) or trade.get('usdcSize', 0) or trade.get('amount', 0) or 0)
        
        if size < WHALE_MIN_INDIVIDUAL_SIZE:
            continue
        
        # Get market info
        market_slug = trade.get('marketSlug', trade.get('slug', trade.get('market', '')))
        outcome = trade.get('outcome', trade.get('asset', 'Unknown'))
        side = trade.get('side', trade.get('type', 'BUY'))
        price = float(trade.get('price', 0) or 0)
        
        # Try to get market question
        market_question = trade.get('title', trade.get('question', ''))
        if not market_question and market_slug:
            market_data = fetch_market_by_slug(market_slug)
            if market_data:
                market_question = market_data.get('question', market_slug)
        
        if not market_question:
            market_question = market_slug or 'Unknown Market'
        
        # Build whale data for consensus tracking
        whale_data = {
            'address': whale_address,
            'name': trader_info.get('name', 'Unknown'),
            'win_rate': trader_info.get('win_rate', 0),
            'tier': trader_info.get('tier', 'UNKNOWN'),
            'rank': trader_info.get('rank', 0),
            'size': size,
            'side': side,
            'outcome': outcome,
            'price': price,
            'market_question': market_question,
            'timestamp': datetime.now().isoformat()
        }
        
        # Check for elite whale solo alert (80%+ WR)
        if trader_info.get('win_rate', 0) >= WHALE_ELITE_MIN_WINRATE:
            trade_data = {
                'market_slug': market_slug,
                'outcome': outcome,
                'side': side,
                'size': size,
                'price': price
            }
            market_url = f"https://polymarket.com/event/{market_slug}"
            alert_elite_whale(trader_info, trade_data, market_question, market_url)
            elite_alerts += 1
        
        # Add to consensus tracking
        if add_whale_position(market_slug, outcome, whale_data):
            new_whale_trades += 1
            logger.info(f"🐋 New whale trade: {trader_info.get('name', 'Unknown')} - ${size:,.0f} on {outcome}")
    
    # Check for consensus alerts
    check_consensus_alerts()
    
    # Log summary
    total_tracked = sum(
        len(whales) 
        for outcomes in whale_positions.values() 
        for whales in outcomes.values()
    )
    
    logger.info(f"🐋 Whale check done: {new_whale_trades} new, {elite_alerts} elite alerts, {total_tracked} total tracked")
    
    # Cleanup old trade hashes (keep last 10000)
    if len(processed_trade_hashes) > 10000:
        processed_trade_hashes.clear()
        logger.info("Cleared processed trade hashes")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 MAIN SCANNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_scan():
    """Run a complete market scan"""
    logger.info("=" * 60)
    logger.info("🔍 SCANNING MARKETS...")
    
    all_markets = []
    offset = 0
    
    while True:
        markets = fetch_markets(MAX_MARKETS_PER_REQUEST, offset)
        if not markets:
            break
        all_markets.extend(markets)
        if len(markets) < MAX_MARKETS_PER_REQUEST:
            break
        offset += MAX_MARKETS_PER_REQUEST
        time.sleep(0.3)
    
    logger.info(f"📊 {len(all_markets)} markets found")
    
    stats = {"safe": 0, "farming": 0}
    
    for market in all_markets:
        result = analyze_market(market)
        
        for opp in result["safe"]:
            alert_safe_bet(opp["market"], opp["probability"], opp["outcome"], opp["days"])
            stats["safe"] += 1
        
        for opp in result["farming"]:
            alert_farming(opp["market"], opp["probability"], opp["outcome"], opp["days"])
            stats["farming"] += 1
    
    # Check whale trades
    check_whale_trades()
    
    logger.info(f"📈 Results: 🟢 SAFE: {stats['safe']} | 🔵 FARMING: {stats['farming']}")
    logger.info("=" * 60)


def main():
    """Main entry point"""
    
    tiers = {}
    for t in TOP_TRADERS.values():
        tier = t.get("tier", "?")
        tiers[tier] = tiers.get(tier, 0) + 1
    
    elite_count = sum(1 for t in TOP_TRADERS.values() if t.get('win_rate', 0) >= WHALE_ELITE_MIN_WINRATE)
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ██████╗  ██████╗ ██╗  ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ██╗  ██╗      ║
║     ██╔══██╗██╔═══██╗██║  ╚██╗ ██╔╝████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝      ║
║     ██████╔╝██║   ██║██║   ╚████╔╝ ██╔████╔██║███████║██████╔╝█████╔╝       ║
║     ██╔═══╝ ██║   ██║██║    ╚██╔╝  ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗       ║
║     ██║     ╚██████╔╝███████╗██║   ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗      ║
║     ╚═╝      ╚═════╝ ╚══════╝╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝      ║
║                                                                              ║
║                    🏆 POLYMARKET WHALE TRACKER 🏆                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🐋 {len(TOP_TRADERS)} WHALES TRACKED:
   👑 LEGENDARY: {tiers.get('LEGENDARY', 0)}
   🏆 ELITE: {tiers.get('ELITE', 0)}
   🥇 TOP: {tiers.get('TOP', 0)}
   🥈 HIGH: {tiers.get('HIGH', 0)}
   🥉 SOLID: {tiers.get('SOLID', 0)}
   📊 VOLUME: {tiers.get('VOLUME', 0)}

📊 ALERTS CONFIGURATION:
   🟢 SAFE BETS: 90-98.5% | <20 days | >$80K liq
   🔵 FARMING: 98.5-99.5% | <4 days | >$65K liq

🐋 WHALE CONSENSUS:
   📍 {WHALE_MIN_CONSENSUS}+ whales same direction → ALERT
   👑 1 whale ≥{WHALE_ELITE_MIN_WINRATE}% WR alone → ALERT
   💰 Minimum ${WHALE_MIN_TOTAL_SIZE} total bet
   ⏰ Window: {WHALE_CONSENSUS_WINDOW_HOURS}h
   🎯 {elite_count} whales can trigger solo

💰 Profit calculations based on ${INVESTMENT_AMOUNT} investment
""")
    
    startup_message = f"""🏆 <b>Polymarket Whale Tracker Started!</b>

📊 SAFE: 90-98.5%
📊 FARMING: 98.5-99.5%

🐋 <b>WHALE CONSENSUS</b>
   • {WHALE_MIN_CONSENSUS}+ whales → consensus alert
   • 1 whale ≥80% WR → solo alert
   • {len(TOP_TRADERS)} whales tracked

💎 Only quality signals!"""
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID, 
            "text": startup_message,
            "parse_mode": "HTML"
        }, timeout=30, verify=False)
    except:
        pass
    
    logger.info(f"🚀 Bot started - scanning every {SCAN_INTERVAL_SECONDS}s")
    
    try:
        while True:
            run_scan()
            logger.info(f"⏳ Next scan in {SCAN_INTERVAL_SECONDS}s...")
            time.sleep(SCAN_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logger.info("\n👋 Bot stopped by user")
        send_telegram("🛑 <b>Bot stopped</b>\n\nSee you soon! 👋")


if __name__ == "__main__":
    main()
