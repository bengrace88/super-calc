import streamlit as st

# --- 1. DATA (Current as of March 2026) ---
# Manual update point: Change these numbers once a month
data = {
    'aus': {'fytd': 7.75, 'last_fy': 13.24, 'one_year': 13.27},
    'int': {'fytd': 1.35, 'last_fy': 14.06, 'one_year': 16.21}
}

# --- 2. UI SETUP ---
st.set_page_config(page_title="Super Scorecard", page_icon="💰")

st.title("📊 Super Return Scorecard")
st.caption("Reporting Period: March 2026")

# Sidebar for Balance
st.sidebar.header("Account Settings")
total_balance = st.sidebar.number_input("Current Balance ($)", value=150000, step=5000)

# Fixed Split as per your request
aus_pct = 25
int_pct = 75

st.sidebar.divider()
st.sidebar.write(f"**Current Split:**")
st.sidebar.write(f"🇦🇺 Australian: {aus_pct}%")
st.sidebar.write(f"🌎 International: {int_pct}%")

# --- 3. CALCULATION FUNCTION ---
def calc_returns(timeframe_key):
    aus_r = data['aus'][timeframe_key]
    int_r = data['int'][timeframe_key]
    
    # Weighted Return %
    weighted_r = (aus_r * (aus_pct/100)) + (int_r * (int_pct/100))
    # Dollar Growth
    dollar_growth = total_balance * (weighted_r / 100)
    
    return weighted_r, dollar_growth

# --- 4. DISPLAY RESULTS ---

# Top Row: The Big Three
col1, col2, col3 = st.columns(3)

# FYTD
r_fytd, d_fytd = calc_returns('fytd')
col1.metric("FYTD", f"${d_fytd:,.0f}", f"{r_fytd:.2f}%")

# Last FY
r_lfy, d_lfy = calc_returns('last_fy')
col2.metric("Last FY", f"${d_lfy:,.0f}", f"{r_lfy:.2f}%")

# Rolling 1 Year
r_1y, d_1y = calc_returns('one_year')
col3.metric("1 Year", f"${d_1y:,.0f}", f"{r_1y:.2f}%")

st.divider()

# Breakdown Detail
st.subheader("Portfolio Value Breakdown")
aus_val = total_balance * (aus_pct / 100)
int_val = total_balance * (int_pct / 100)

st.write(f"**Australian Component ({aus_pct}%):** ${aus_val:,.2f}")
st.write(f"**International Component ({int_pct}%):** ${int_val:,.2f}")

st.info("To update these rates in the future, just edit the 'data' dictionary at the top of your app.py file in GitHub.")
