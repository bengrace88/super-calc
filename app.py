import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape the data
def get_super_data():
    url = "https://www.australiansuper.com/why-choose-us/investment-performance?superType=Super&display=table"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 1:
                name = cells[0].text.strip()
                # Scraping the '1 Year' return (typically column 4)
                if "Australian Shares" in name:
                    data['aus'] = float(cells[3].text.replace('%', '').strip())
                if "International Shares" in name:
                    data['int'] = float(cells[3].text.replace('%', '').strip())
        return data
    except:
        return None

# App Interface
st.set_page_config(page_title="Super Calc", page_icon="📈")
st.title("💰 Super Return Calc")

perf = get_super_data()

if perf:
    st.subheader("Adjust Your Split")
    aus_pct = st.slider("Australian Shares (%)", 0, 100, 50)
    int_pct = 100 - aus_pct
    st.info(f"International Shares: {int_pct}%")

    # The Math
    weighted_return = (perf['aus'] * (aus_pct/100)) + (perf['int'] * (int_pct/100))

    st.divider()
    st.metric(label="Estimated 1-Year Return", value=f"{weighted_return:.2f}%")
    
    # Show the raw rates for transparency
    col1, col2 = st.columns(2)
    col1.caption(f"Aus Rate: {perf['aus']}%")
    col2.caption(f"Int Rate: {perf['int']}%")
else:
    st.error("Could not fetch latest rates. Check back short
    ly!")
