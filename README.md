# 🏆 Polymarket Whale Tracker

A powerful Telegram bot that scans [Polymarket](https://polymarket.com) for high-probability trading opportunities and tracks whale movements in real-time.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🟢 Safe Bets
Alerts for markets with 90-98.5% probability, high liquidity (>$80K), and resolution within 20 days.

### 🔵 Volume Farming  
Alerts for very high probability markets (98.5-99.5%) resolving within 4 days - perfect for quick turnovers.

### 🐋 Whale Tracking
- **42 top traders** monitored in real-time
- **Consensus alerts**: When 5+ whales bet on the same outcome
- **Elite alerts**: When a single whale with 80%+ win rate makes a move

## 🐋 Tracked Whales

| Tier | Count | Description |
|------|-------|-------------|
| 👑 LEGENDARY | 3 | 95%+ win rate |
| 🏆 ELITE | 7 | 85-95% win rate |
| 🥇 TOP | 1 | 80-85% win rate |
| 🥈 HIGH | 7 | 70-80% win rate |
| 🥉 SOLID | 16 | 60-70% win rate |
| 📊 VOLUME | 8 | High volume traders |

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Gazettebale/polymarket-whale-tracker.git
cd polymarket-whale-tracker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your Telegram credentials:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

**How to get these:**
1. Create a bot with [@BotFather](https://t.me/BotFather) on Telegram
2. Get your chat ID from [@userinfobot](https://t.me/userinfobot)

### 4. Run the bot

```bash
python bot.py
```

To stop: Press `Ctrl + C`

## ⚙️ Configuration

Edit the config section in `bot.py` to customize:

| Setting | Default | Description |
|---------|---------|-------------|
| `SAFE_MIN_PROBABILITY` | 0.90 | Minimum probability for SAFE alerts |
| `SAFE_MAX_PROBABILITY` | 0.985 | Maximum probability for SAFE alerts |
| `SAFE_MIN_LIQUIDITY` | $80K | Minimum liquidity for SAFE alerts |
| `SAFE_MAX_DAYS_TO_RESOLUTION` | 20 | Max days until resolution |
| `FARMING_MIN_PROBABILITY` | 0.985 | Minimum probability for FARMING |
| `FARMING_MAX_PROBABILITY` | 0.995 | Maximum probability for FARMING |
| `FARMING_MIN_LIQUIDITY` | $65K | Minimum liquidity for FARMING |
| `WHALE_MIN_CONSENSUS` | 5 | Min whales for consensus alert |
| `WHALE_ELITE_MIN_WINRATE` | 80% | Min win rate for solo alert |
| `SCAN_INTERVAL_SECONDS` | 120 | Time between scans |

You can also set these via environment variables:
```env
INVESTMENT_AMOUNT=1000
SCAN_INTERVAL=60
```

## 📱 Telegram Alerts

### Safe Bet Alert
```
🟢 SAFE BET OPPORTUNITY 🟢

📊 Will Bitcoin reach $100K by Dec 31?

━━━━━━━━━━━━━━━━━━━━━━

🎯 Bet: Yes
📈 Probability: 94.5%
⏰ Resolution: 3 days

━━━━━━━━━━━━━━━━━━━━━━

💰 With $500:
   Potential profit: $29.10 (+5.8%)

💧 Liquidity: $250,000
📊 Volume: $1,500,000
```

### Elite Whale Alert
```
👑 ELITE WHALE ALERT 👑

━━━━━━━━━━━━━━━━━━━━━━

👤 LlamaEnjoyer
   Tier: LEGENDARY
   Win Rate: 96.0%
   Rank: #69

━━━━━━━━━━━━━━━━━━━━━━

🟢 BUY Yes
💵 Size: $5,000.00
📈 Price: 65.0%
```

## 🖥️ Running 24/7

### Using screen (Linux/Mac)
```bash
screen -S polymarket
python bot.py
# Press Ctrl+A then D to detach
```

### Using PM2 (Node.js process manager)
```bash
npm install -g pm2
pm2 start bot.py --interpreter python3 --name polymarket
pm2 save
```

### Cloud Options
- **Railway** - Easy deployment, free tier available
- **Heroku** - Classic choice for Python bots
- **DigitalOcean** - $5/month droplet
- **AWS EC2** - Free tier available

## 📊 Stats Scripts

View your alert statistics:

```bash
# View notification stats
python view_stats.py

# View detailed alert stats
python view_alert_stats.py
```

## 🔧 Troubleshooting

**Bot won't start?**
- Make sure Python 3.8+ is installed
- Make sure dependencies are installed: `pip install -r requirements.txt`
- Check your `.env` file exists and has valid credentials

**No Telegram messages?**
- Verify your bot token is correct
- Make sure you've started a conversation with your bot
- Check if your chat ID is correct

**API errors?**
- Polymarket API may be blocked in some regions - try using a VPN
- Check your internet connection

## ⚠️ Disclaimer

This bot is for **informational purposes only**. 

- Trading involves risk of financial loss
- Past whale performance doesn't guarantee future results
- Do your own research before making any trades
- Never invest more than you can afford to lose

## 📄 License

MIT License - feel free to modify and use as you wish!

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

Made with 💰 by [@_Gazettebale](https://twitter.com/_Gazettebale)
