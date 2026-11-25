import os
import warnings
import pandas as pd
import requests
import yfinance as yf

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

warnings.simplefilter(action="ignore", category=FutureWarning)

SP500_TICKERS = [
    "MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL", "A",
    "APD", "ABNB", "AKAM", "ALB", "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL",
    "GOOG", "MO", "AMZN", "AMCR", "AEE", "AEP", "AXP", "AIG", "AMT", "AWK",
    "AMP", "AME", "AMGN", "APH", "ADI", "ANSS", "AON", "APA", "APO", "AAPL",
    "AMAT", "APTV", "ACGL", "ADM", "ANET", "AJG", "AIZ", "T", "ATO", "ADSK",
    "ADP", "AZO", "AVB", "AVY", "AXON", "BKR", "BALL", "BAC", "BAX", "BDX",
    "BRK-B", "BBY", "TECH", "BIIB", "BLK", "BX", "BA", "BKNG", "BWA",
    "BSX", "BMY", "AVGO", "BR", "BRO", "BF-B", "BLDR", "BG", "BXP", "CHRW",
    "CDNS", "CZR", "CPT", "CPB", "COF", "CAH", "KMX", "CCL", "CARR", "CAT",
    "CBOE", "CBRE", "CDW", "CE", "COR", "CNC", "CNP", "CF", "CRL", "SCHW",
    "CHTR", "CVX", "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C",
    "CFG", "CLX", "CME", "CMS", "KO", "CTSH", "CL", "CMCSA", "CAG", "COP",
    "ED", "STZ", "CEG", "COO", "CPRT", "GLW", "CPAY", "CTVA", "CSGP", "COST",
    "CRWD", "CCI", "CSX", "CMI", "CVS", "DHR", "DRI", "DVA",
    "DECK", "DE", "DELL", "DAL", "DVN", "DXCM", "FANG", "DLR", "DG",
    "DLTR", "D", "DPZ", "DOV", "DOW", "DHI", "DTE", "DUK", "DD", "EMN",
    "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "ELV", "EMR", "ENPH", "ETR",
    "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR", "ERIE", "ESS", "EL", "EG",
    "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FDS", "FICO",
    "FAST", "FRT", "FDX", "FIS", "FITB", "FSLR", "FE", "FMC", "F",
    "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX", "GRMN", "IT", "GE", "GEHC",
    "GEV", "GEN", "GNRC", "GD", "GIS", "GM", "GPC", "GILD", "GPN", "GL",
    "GDDY", "GS", "HAL", "HIG", "HAS", "HCA", "DOC", "HSIC", "HSY",
    "HPE", "HLT", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUBB",
    "HUM", "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW", "INCY", "IR", "PODD",
    "INTC", "ICE", "IFF", "IP", "INTU", "ISRG", "IVZ", "INVH", "IQV",
    "IRM", "JBHT", "JBL", "JKHY", "J", "JNJ", "JCI", "JPM",
    "KVUE", "KDP", "KEY", "KEYS", "KMB", "KIM", "KMI", "KKR", "KLAC", "KHC",
    "KR", "LHX", "LH", "LRCX", "LW", "LVS", "LDOS", "LEN", "LII", "LLY",
    "LIN", "LYV", "LKQ", "LMT", "L", "LOW", "LULU", "LYB", "MTB", "MPC",
    "MKTX", "MAR", "MLM", "MAS", "MA", "MTCH", "MKC", "MCD", "MCK",
    "MDT", "MRK", "META", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA",
    "MRNA", "MHK", "MOH", "TAP", "MDLZ", "MPWR", "MNST", "MCO", "MS", "MOS",
    "MSI", "MSCI", "NDAQ", "NTAP", "NFLX", "NEM", "NWSA", "NWS", "NEE", "NKE",
    "NI", "NDSN", "NSC", "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "NVR",
    "NXPI", "ORLY", "OXY", "ODFL", "OMC", "ON", "OKE", "ORCL", "OTIS", "PCAR",
    "PKG", "PLTR", "PANW", "PARA", "PH", "PAYX", "PAYC", "PYPL", "PNR", "PEP",
    "PFE", "PCG", "PM", "PSX", "PNW", "PNC", "POOL", "PPG", "PPL", "PFG",
    "PG", "PGR", "PLD", "PRU", "PEG", "PTC", "PSA", "PHM", "QRVO", "PWR",
    "QCOM", "DGX", "RL", "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG",
    "RMD", "RVTY", "ROK", "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC",
    "SLB", "STX", "SRE", "NOW", "SHW", "SPG", "SWKS", "SJM", "SW", "SNA",
    "SOLV", "SO", "LUV", "SWK", "SBUX", "STT", "STLD", "STE", "SYK", "SMCI",
    "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL",
    "TDY", "TFX", "TER", "TSLA", "TXN", "TPL", "TXT", "TMO", "TJX", "TSCO",
    "TT", "TDG", "TRV", "TRMB", "TFC", "TYL", "TSN", "USB", "UBER", "UDR",
    "ULTA", "UNP", "UAL", "UPS", "URI", "UNH", "UHS", "VLO", "VTR", "VLTO",
    "VRSN", "VRSK", "VZ", "VRTX", "VTRS", "VICI", "V", "VST", "VMC", "WRB",
    "GWW", "WAB", "WMT", "DIS", "WBD", "WM", "WAT", "WEC", "WFC",
    "WELL", "WST", "WDC", "WY", "WMB", "WTW", "WDAY", "WYNN", "XEL", "XYL",
    "YUM", "ZBRA", "ZBH", "ZTS"
]


def send_telegram_alert(message_text):
    """Sends a formatted message to your Telegram bot."""
    base = "https://" + "api.telegram.org"
    endpoint = "/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
    url = base + endpoint

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "Markdown",
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("\n✅ Telegram alert sent!")
        else:
            print(f"\n⚠️ Telegram error: {response.text}")
    except Exception as e:
        print(f"\n⚠️ Failed to connect to Telegram: {e}")


class NewsomeSp500Agent:

    def __init__(self, tickers):
        self.tickers = tickers

    def fetch_data(self, ticker, period="2y"):
        """Fetches historical daily data and removes any blank placeholder rows."""
        try:
            df = yf.download(
                ticker,
                period=period,
                progress=False,
                group_by="ticker",
                auto_adjust=True,
            )
            if isinstance(df.columns, pd.MultiIndex):
                df = df[ticker]
            df = df.dropna(subset=["Close"])
            return df
        except Exception:
            return None

    def get_market_regime(self):
        """Checks SPY against its Daily 50 and 200 SMAs for broad market health."""
        df = self.fetch_data("SPY", period="1y")
        if df is None or df.empty or len(df) < 200:
            return "⚪ *Market Status:* Unavailable"

        spy_close = float(df["Close"].iloc[-1])
        spy_sma50 = float(df["Close"].rolling(window=50).mean().iloc[-1])
        spy_sma200 = float(df["Close"].rolling(window=200).mean().iloc[-1])

        if spy_close > spy_sma50 and spy_close > spy_sma200:
            return f"🟢 *Market Status:* BULLISH (SPY `${spy_close:.2f}` > 50 & 200 SMA)"
        elif spy_close > spy_sma200:
            return f"🟡 *Market Status:* CAUTION — SPY `${spy_close:.2f}` below 50 SMA (`${spy_sma50:.2f}`)"
        else:
            return f"🔴 *Market Status:* HIGH RISK — SPY `${spy_close:.2f}` below 200 SMA (`${spy_sma200:.2f}`)"

    def calculate_indicators(self, df):
        """Calculates Daily 100/200 SMAs, 20 EMA, and Weekly 50 SMA."""
        df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
        df["SMA100"] = df["Close"].rolling(window=100).mean()
        df["SMA200"] = df["Close"].rolling(window=200).mean()

        weekly_close = df["Close"].resample("W-FRI").last()
        weekly_sma50 = weekly_close.rolling(window=50).mean()
        df.attrs["WEEKLY_SMA50"] = (
            float(weekly_sma50.iloc[-1]) if len(weekly_sma50) >= 50 else None
        )
        return df

    def check_bullish_criteria(self, df):
        """Applies Newsome's Weekly + Daily Trend, Pullback, Reversal & Volume Formula."""
        weekly_sma50 = df.attrs.get("WEEKLY_SMA50")
        if (
            len(df) < 200
            or "SMA200" not in df.columns
            or weekly_sma50 is None
            or pd.isna(weekly_sma50)
        ):
            return None

        today = df.iloc[-1]
        yesterday = df.iloc[-2]

        close_today = float(today["Close"])
        open_today = float(today["Open"])
        vol_today = float(today["Volume"])
        low_today = float(today["Low"])

        close_yesterday = float(yesterday["Close"])
        open_yesterday = float(yesterday["Open"])
        high_yesterday = float(yesterday["High"])
        low_yesterday = float(yesterday["Low"])
        vol_yesterday = float(yesterday["Volume"])

        sma100 = float(today["SMA100"])
        sma200 = float(today["SMA200"])

        is_weekly_uptrend = close_today > weekly_sma50
        is_daily_uptrend = close_today > sma100 and close_today > sma200
        was_pullback = close_yesterday < open_yesterday
        is_bull_reversal = (
            close_today > open_today and close_today > high_yesterday
        )
        strong_volume = vol_today > vol_yesterday

        if (
            is_weekly_uptrend
            and is_daily_uptrend
            and was_pullback
            and is_bull_reversal
            and strong_volume
        ):
            entry_price = close_today
            stop_loss = min(low_today, low_yesterday)
            risk = entry_price - stop_loss

            if risk > 0:
                target_price = entry_price + (1.2 * risk)
                return {
                    "Signal": "HIGH-PROBABILITY BULLISH REVERSAL",
                    "Entry": round(entry_price, 2),
                    "Stop Loss": round(stop_loss, 2),
                    "Target (1.2R)": round(target_price, 2),
                }
        return None

    def scan_market(self):
        """Scans the entire cleaned S&P 500 list for trade setups."""
        market_status = self.get_market_regime()
        print(market_status)
        print(f"Beginning scan across {len(self.tickers)} S&P 500 stocks...")
        matches = {}

        for i, ticker in enumerate(self.tickers):
            df = self.fetch_data(ticker)
            if df is not None and not df.empty and len(df) >= 200:
                df = self.calculate_indicators(df)
                setup = self.check_bullish_criteria(df)
                if setup:
                    matches[ticker] = setup
                    print(f" -> Found setup for {ticker}!")

            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{len(self.tickers)} stocks...")

        return market_status, matches


if __name__ == "__main__":
    agent = NewsomeSp500Agent(SP500_TICKERS)
    market_status, results = agent.scan_market()

   if results:
        alert_lines = [
            "📈 *Newsome S&P 500 Swing Setups* 📈",
            market_status,
            "",
        ]
        for stock, details in results.items():
            print(f"\n★ Setup Found for {stock} ★")
            alert_lines.append(f"*{stock}* — Bullish Reversal (Weekly+Daily)")
            for k, v in details.items():
                print(f"  {k}: {v}")
                if k != "Signal":
                    alert_lines.append(f"  • {k}: `${v}`")
            alert_lines.append("")

        send_telegram_alert("\n".join(alert_lines))
    else:
        msg = "No S&P 500 stocks matched the Weekly 50 SMA + pullback + volume criteria today."
        print(f"\n{msg}")
        send_telegram_alert(f"📊 *Newsome Scanner*\n{market_status}\n\n{msg}")
