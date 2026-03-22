import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_super_data():
    url = "https://www.australiansuper.com/why-choose-us/investment-performance?superType=Super&display=table"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 3:
                name = cells[0].text.strip()
                # Scrape 1-Year Performance (Column 4)
                if "Australian Shares" in name:
                    data['aus_rate'] = float(cells[3].text.replace('%', '').strip())
                if "International Shares" in name:
                    data['int_rate'] = float(cells[3].text.replace('%', '').strip())
        return data
    except:
        # Fallback rates if scraping fails
        return {'aus_rate': 13.24, 'int_rate': 14.06, 'is_fallback': True}

# --- UI Setup ---
st.set_page_config(page_title="Super Calc", page_icon="💰")
st.title("📊 My Super Tracker")

perf = get_super_data()

# 1. Input Section
st.subheader("Your Portfolio Details")
total_balance = st.number_input("Total Super Balance ($)", min_value=0, value=100000, step=1000)

col_a, col_b = st.columns(2)
with col_a:
    aus_split = st.slider("Aus Shares %", 0, 100, 50)
with col_b:
    int_split = 100 - aus_split
    st.write(f"\n\n**Int Shares:** {int_split}%")

# 2. Calculation Logic
aus_dollars = total_balance * (aus_split / 100)
int_dollars = total_balance * (int_split / 100)

aus_profit = aus_dollars * (perf['aus_rate'] / 100)
int_profit = int_dollars * (perf['int_rate'] / 100)

total_profit = aus_profit + int_profit
weighted_return = (total_profit / total_balance) * 100 if total_balance > 0 else 0

# 3. Results Display
st.divider()
st.metric(label="Approx. 1-Year Growth", value=f"${total_profit:,.2f}", delta=f"{weighted_return:.2f}%")

# Break down the holdings
st.write("### Portfolio Breakdown")
st.write(f"* **Australian Holdings:** ${aus_dollars:,.0f} (@ {perf['aus_rate']}%)")
st.write(f"* **International Holdings:** ${int_dollars:,.0f} (@ {perf['int_rate']}%)")

if perf.get('is_fallback'):
    st.warning("Using last known market rates (Live site blocked).")
else:
    st.success("Live rates synced.")
