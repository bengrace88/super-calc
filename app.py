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
            if len(cells) > 5:
                name = cells[0].text.strip()
                # Mapping columns based on the AustralianSuper table structure
                # Col 1: FYTD | Col 2: Last FY | Col 3: 1 Year
                if "Australian Shares" in name:
                    data['aus'] = {
                        'fytd': float(cells[1].text.replace('%', '').strip()),
                        'last_fy': float(cells[2].text.replace('%', '').strip()),
                        'one_year': float(cells[3].text.replace('%', '').strip())
                    }
                if "International Shares" in name:
                    data['int'] = {
                        'fytd': float(cells[1].text.replace('%', '').strip()),
                        'last_fy': float(cells[2].text.replace('%', '').strip()),
                        'one_year': float(cells[3].text.replace('%', '').strip())
                    }
        return data
    except:
        return None

# --- UI Setup ---
st.set_page_config(page_title="Super Tracker", page_icon="📈")
st.title("🚀 Super Performance Dashboard")

perf = get_super_data()

if perf:
    # 1. Inputs
    st.sidebar.header("Settings")
    total_balance = st.sidebar.number_input("Current Balance ($)", value=150000, step=5000)
    aus_pct = st.sidebar.slider("Aus Shares Split %", 0, 100, 50)
    int_pct = 100 - aus_pct

    # 2. Timeframe Selector
    timeframe = st.radio(
        "Select Performance Period for Calculation:",
        ["Financial Year to Date (FYTD)", "Last Financial Year", "Rolling 1 Year"],
        horizontal=True
    )

    # Map selection to data keys
    key_map = {"Financial Year to Date (FYTD)": "fytd", "Last Financial Year": "last_fy", "Rolling 1 Year": "one_year"}
    active_key = key_map[timeframe]

    # 3. Calculation
    aus_r = perf['aus'][active_key]
    int_r = perf['int'][active_key]
    
    weighted_r = (aus_r * (aus_pct/100)) + (int_r * (int_pct/100))
    profit = total_balance * (weighted_r / 100)

    # 4. Results Display
    st.divider()
    st.metric(label=f"Estimated {timeframe} Return", value=f"${profit:,.2f}", delta=f"{weighted_r:.2f}%")

    # 5. Comparison Table
    st.subheader("Market Comparison (%)")
    st.table({
        "Metric": ["FYTD", "Last FY", "Rolling 1 Year"],
        "Australian Shares": [f"{perf['aus']['fytd']}%", f"{perf['aus']['last_fy']}%", f"{perf['aus']['one_year']}%"],
        "International Shares": [f"{perf['int']['fytd']}%", f"{perf['int']['last_fy']}%", f"{perf['int']['one_year']}%"]
    })

    st.success("Live data synced from AustralianSuper.")
else:
    st.error("Site is being shy. Using fallback display.")
    
