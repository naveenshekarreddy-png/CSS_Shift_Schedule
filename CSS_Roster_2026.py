import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# CSS for a professional look
st.markdown(
    """
    <style>
    .stApp { background: #f8fafc; }
    .main-title { color: #1e40af; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>🛡️ High-Consistency Team Roster</h1>", unsafe_allow_html=True)

# Team Data from your provided list
staff_data = {
    "L2": ["Arsalan Shaikh", "Akash Sahu", "Mahadev Bhusnar", "Gandharv Adhikari", "Mehmood Nachan", "Manoj Khatri", "Mahesh Pawar", "Pranav Markande", "Nitin Gadekar", "Fernando Gerard", "Athira Pillai", "Abhijeet Gorivale"],
    "L3": ["Ashish Chaturvedi", "Ranjit Kumar S P", "Arjun Ghadi", "Sanjiv Sudhakar", "Varad C N"],
    "TL": ["Durgeshkumar Singh", "Mahesh Arokia", "Mehul Dholakiya", "Atul Dhamal", "Paras Shah", "Rajkumar Chitravelu", "Vigneshwaran Prakash"]
}
all_staff = [name for tier in staff_data.values() for name in tier]

with st.sidebar:
    st.header("Roster Parameters")
    start_date = st.date_input("Start Date", datetime.now())
    duration = st.slider("Duration (Days)", 7, 31, 30)
    target_shifts = st.slider("Target Shifts/Person", 10, 25, 20)
    on_leave = st.multiselect("Staff on Holiday", all_staff)

def generate_optimized_roster():
    shift_counts = {name: 0 for name in all_staff}
    consecutive_days = {name: 0 for name in all_staff}
    last_shift_type = {name: None for name in all_staff}
    roster_records = []

    for i in range(duration):
        current_day = start_date + timedelta(days=i)
        daily_selections = set()

        def pick_staff(tier, count, shift_type, already_selected):
            # 1. Eligibility Filter
            eligible = [
                s for s in staff_data[tier] 
                if s not in on_leave 
                and s not in already_selected 
                and consecutive_days[s] < 6  # HARD LIMIT: Max 6 days
                and shift_counts[s] < target_shifts
            ]

            # 2. Logic: Prioritize those who have worked 1-4 days on THIS same shift
            # This forces the "5 days in same shift" rule
            priority_continuing = [
                s for s in eligible 
                if last_shift_type[s] == shift_type and 0 < consecutive_days[s] < 5
            ]
            
            # 3. Secondary: Those who have worked 5 days but can do a 6th if needed
            priority_buffer = [
                s for s in eligible 
                if last_shift_type[s] == shift_type and consecutive_days[s] == 5
            ]

            # 4. Others: Fresh staff or those coming off a break (sorted by least shifts for equality)
            others = [s for s in eligible if s not in priority_continuing and s not in priority_buffer]
            others.sort(key=lambda x: shift_counts[x])

            # Combine pools: Keep going -> New/Fresh -> Buffer (6th day)
            pool = priority_continuing + others + priority_buffer
            selection = pool[:count]

            for s in selection:
                shift_counts[s] += 1
                consecutive_days[s] += 1
                last_shift_type[s] = shift_type
                already_selected.add(s)
            return selection

        # Shift Assignments (1 TL, 1 L3, 2 L2)
        d_tl = pick_staff("TL", 1, "Day", daily_selections)
        d_l3 = pick_staff("L3", 1, "Day", daily_selections)
        d_l2 = pick_staff("L2", 2, "Day", daily_selections)

        n_tl = pick_staff("TL", 1, "Night", daily_selections)
        n_l3 = pick_staff("L3", 1, "Night", daily_selections)
        n_l2 = pick_staff("L2", 2, "Night", daily_selections)

        # Update rest status for those not working
        for name in all_staff:
            if name not in daily_selections:
                consecutive_days[name] = 0
                last_shift_type[name] = None

        roster_records.append({
            "Date": current_day.strftime("%Y-%m-%d"),
            "Day": current_day.strftime("%A"),
            "☀️ Day Shift": f"{', '.join(d_tl)} | {', '.join(d_l3)} | {', '.join(d_l2)}",
            "🌙 Night Shift": f"{', '.join(n_tl)} | {', '.join(n_l3)} | {', '.join(n_l2)}"
        })

    return pd.DataFrame(roster_records), shift_counts

if st.button("🚀 Generate Optimized Roster"):
    df, stats = generate_optimized_roster()
    st.table(df)
    
    st.subheader("📊 Workload Balance Statistics")
    st.dataframe(pd.DataFrame(list(stats.items()), columns=["Staff", "Shifts"]))