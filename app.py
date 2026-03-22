import streamlit as st

# --- UI SETUP ---
st.set_page_config(page_title="Super Input", page_icon="📝", layout="wide")

st.title("📊 My Super Dashboard")
st.write("Enter the latest figures to see your 25/75 split performance.")

# --- 1. THE DATA PROMPTS (The "Inputs") ---
# We use columns to keep the input fields neat on your phone
col1, col2 = st.columns(2)

with col1:
    total_balance = st.number_input("Current Super Balance ($)", min_value=0.0, value=150000.0, step=1000.0)
    
with col2:
    # We ask for the "Return to Date" (FYTD) specifically as you requested
    aus_return_input = st.number_input("AU Shares Return to Date (%)", value=7.75, step=0.01)
    int_return_input = st.number_input("INT Shares Return to Date (%)", value=1.35, step=0.01)

# --- 2. THE LOGIC (The "Engine") ---
# Your fixed split
aus_weight = 0.25
int_weight = 0.75

# Weighted Calculation
combined_return_pct = (aus_return_input * aus_weight) + (int_return_input * int_weight)
total_dollar_gain = total_balance * (combined_return_pct / 100)

# Portfolio values
aus_value = total_balance * aus_weight
int_value = total_balance * int_weight

# --- 3. THE DASHBOARD (The "Output") ---
st.divider()

# Big "Hero" Metrics
m1, m2 = st.columns(2)
m1.metric("Total Combined Return", f"{combined_return_pct:.2f}%")
m2.metric("Estimated Profit/Loss", f"${total_dollar_gain:,.2f}")

# Progress Bar toward a milestone (Engineers love a progress bar)
target = 500000.0
progress = min(total_balance / target, 1.0)
st.write(f"### Progress to ${target:,.0f} Milestone")
st.progress(progress)
st.caption(f"Currently at {progress*100:.1f}% of your goal.")

# Breakdown Table
st.subheader("Current Asset Allocation")
st.table({
    "Asset Class": ["Australian Shares (25%)", "International Shares (75%)", "TOTAL"],
    "Value ($)": [f"${aus_value:,.2f}", f"${int_val:,.2f}", f"${total_balance:,.2f}"],
    "Return Contribution": [f"{(aus_return_input * aus_weight):.2f}%", f"{(int_return_input * int_weight):.2f}%", f"{combined_return_pct:.2f}%"]
})

st.info("💡 Tip: Just check your AustralianSuper app once a month, punch the new % numbers in here, and see your instant weighted growth.")
