import streamlit as st

# --- 1. DATA (March 2026 Actuals) ---
# I've updated these to match the latest AustralianSuper March 2026 table
data = {
    'aus': {
        'fytd': 7.75,       # FYTD to 12 Mar 2026
        'last_fy': 13.24,   # Full 2024-25 FY
        'one_year': 13.27   # Rolling 12 months
    },
    'int': {
        'fytd': 1.35,       # FYTD to 12 Mar 2026
        'last_fy': 14.06,   # Full 2024-25 FY
        'one_year': 16.21   # Rolling 12 months
    }
}

# --- 2. UI SETUP ---
st.set_page_config(page_title="Super Tracker", page_icon="📈", layout="centered")

st.title("🚀 My Super Performance")
st.caption("Data as of March 2026")

# Sidebar for Inputs
st.sidebar.header("Portfolio Settings")
total_balance = st.sidebar.number_input("Current Balance ($)", value=150000, step=5000)
aus_pct = st.sidebar.slider("Australian Shares %", 0, 100, 50)
int_pct = 100 - aus_pct
st.sidebar.info(f"International Split: {int_pct}%")

# Timeframe Selector
timeframe = st.radio(
    "Select Performance Period:",
    ["Financial Year to Date (FYTD)", "Last Financial Year", "Rolling 1 Year"],
    horizontal=True
)

# Map selection to data keys
key_map = {
    "Financial Year to Date (FYTD)": "fytd", 
    "Last Financial Year": "last_fy", 
    "Rolling 1 Year": "one_year"
}
active_key = key_map[timeframe]

# --- 3. CALCULATIONS ---
aus_rate = data['aus'][active_key]
int_rate = data['int'][active_key]

weighted_return_pct = (aus_rate * (aus_pct/100)) + (int_rate * (int_pct/100))
dollar_growth = total_balance * (weighted_return_pct / 100)

# --- 4. DISPLAY ---
st.divider()
st.metric(
    label=f"Estimated {timeframe} Growth", 
    value=f"${dollar_growth:,.2f}", 
    delta=f"{weighted_return_pct:.2f}%"
)

# Show Breakdown Table
st.subheader("Historical Context (%)")
comparison_data = {
    "Period": ["FYTD", "Last FY", "1 Year"],
    "AU Shares": [f"{data['aus']['fytd']}%", f"{data['aus']['last_fy']}%", f"{data['aus']['one_year']}%"],
    "INT Shares": [f"{data['int']['fytd']}%", f"{data['int']['last_fy']}%", f"{data['int']['one_year']}%"]
}
st.table(comparison_data)

st.warning("Note: Site scraping is currently disabled to prevent IP blocking. Rates are updated manually for March 2026.")
