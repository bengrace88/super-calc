import streamlit as st

# --- UI SETUP ---
st.set_page_config(page_title="Super Dashboard", page_icon="💰", layout="centered")

st.title("📊 My Super Dashboard")

# --- 1. THE QUICK LINK SECTION ---
st.info("Step 1: Get the latest 'FYTD' returns from the table below.")
# This creates a prominent button that opens the target URL
st.link_button("🔗 Open AustralianSuper Performance Table", "https://www.australiansuper.com/why-choose-us/investment-performance?superType=Super&display=table")

st.divider()

# --- 2. THE DATA PROMPTS ---
st.subheader("Step 2: Enter Today's Figures")
col1, col2 = st.columns(2)

with col1:
    total_balance = st.number_input("Current Super Balance ($)", min_value=0.0, value=150000.0, step=1000.0)
    
with col2:
    # Pre-filled with current March 2026 estimates
    aus_return_input = st.number_input("AU Shares FYTD (%)", value=7.75, step=0.01)
    int_return_input = st.number_input("INT Shares FYTD (%)", value=1.35, step=0.01)

# --- 3. THE LOGIC ---
# Your 25/75 Split
aus_weight = 0.25
int_weight = 0.75

# Calculations
combined_return_pct = (aus_return_input * aus_weight) + (int_return_input * int_weight)
total_dollar_gain = total_balance * (combined_return_pct / 100)

# Portfolio values
aus_value = total_balance * aus_weight
int_value = total_balance * int_weight

# --- 4. THE RESULTS ---
st.divider()

# Metrics
m1, m2 = st.columns(2)
m1.metric("Combined FYTD Return", f"{combined_return_pct:.2f}%")
m2.metric("Estimated FYTD Profit", f"${total_dollar_gain:,.2f}")

# Progress Bar
target = 500000.0
progress = min(total_balance / target, 1.0)
st.write(f"### Progress to ${target:,.0f} Goal")
st.progress(progress)
st.caption(f"You are {progress*100:.1f}% of the way to your milestone.")

# Detail Table
with st.expander("View Allocation Breakdown"):
    st.table({
        "Asset Class": ["Australian Shares (25%)", "International Shares (75%)"],
        "Value ($)": [f"${aus_value:,.2f}", f"${int_value:,.2f}"],
        "Profit Contrib. ($)": [f"${(aus_value * aus_return_input / 100):,.2f}", f"${(int_value * int_return_input / 100):,.2f}"]
    })
