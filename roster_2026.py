import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="24/7 Team Roster Pro", layout="wide")

# Staff Data Organized by Tier
staff_data = {
    "L2": ["Arsalan Shaikh", "Akash Sahu", "Mahadev Bhusnar", "Gandharv Adhikari", "Mehmood Nachan", "Manoj Khatri", "Mahesh Pawar", "Pranav Markande", "Nitin Gadekar", "Fernando Gerard", "Athira Pillai", "Abhijeet Gorivale"],
    "L3": ["Ashish Chaturvedi", "Ranjit Kumar S P", "Arjun Ghadi", "Sanjiv Sudhakar", "Varad C N"],
    "TL": ["Durgeshkumar Singh", "Mahesh Arokia", "Mehul Dholakiya", "Atul Dhamal", "Paras Shah", "Rajkumar Chitravelu", "Vigneshwaran Prakash"]
}

all_staff_names = [name for tier in staff_data.values() for name in tier]

st.title("🌙 ☀️ 24/7 Automated Roster with Stats")

with st.sidebar:
    st.header("1. General Settings")
    start_date = st.date_input("Start Date", datetime.now())
    duration = st.slider("Roster Duration (Days)", 7, 31, 14)
    
    st.divider()
    st.header("2. Leave Management")
    on_leave = st.multiselect("Select Staff on Holiday/Leave:", all_staff_names)
    
    st.divider()
    st.header("3. Shift Ratios")
    l2_count = st.number_input("L2s per shift", 2, 3, 2)
    l3_count = st.number_input("L3s per shift", 1, 2, 1)

def generate_roster():
    consecutive_days = {name: 0 for name in all_staff_names}
    last_shift = {name: None for name in all_staff_names}
    shift_counts = {name: 0 for name in all_staff_names} # Tracker for Stats
    
    roster_records = []

    for i in range(duration):
        current_day = start_date + timedelta(days=i)
        available_today = [s for s in all_staff_names if s not in on_leave and consecutive_days[s] < 6]
        
        def pick_for_shift(shift_name, already_selected):
            picked = {}
            for tier, members in staff_data.items():
                needed = 1 if tier == "TL" else (l3_count if tier == "L3" else l2_count)
                eligible = [s for s in members if s in available_today and s not in already_selected]
                
                # Priority logic for consistency
                priority = [s for s in eligible if last_shift[s] == shift_name and consecutive_days[s] > 0]
                others = [s for s in eligible if s not in priority]
                
                pool = priority + random.sample(others, len(others))
                selection = pool[:int(needed)]
                picked[tier] = selection
                already_selected.update(selection)
            return picked

        daily_selections = set()
        day_team = pick_for_shift("Day", daily_selections)
        night_team = pick_for_shift("Night", daily_selections)

        for name in all_staff_names:
            if name in daily_selections:
                consecutive_days[name] += 1
                shift_counts[name] += 1
                last_shift[name] = "Day" if any(name in day_team[t] for t in day_team) else "Night"
            else:
                consecutive_days[name] = 0
                last_shift[name] = None

        roster_records.append({
            "Date": current_day.strftime("%Y-%m-%d"),
            "Day": current_day.strftime("%A"),
            "☀️ DAY: TL": ", ".join(day_team["TL"]),
            "☀️ DAY: L3": ", ".join(day_team["L3"]),
            "☀️ DAY: L2": ", ".join(day_team["L2"]),
            "🌙 NIGHT: TL": ", ".join(night_team["TL"]),
            "🌙 NIGHT: L3": ", ".join(night_team["L3"]),
            "🌙 NIGHT: L2": ", ".join(night_team["L2"]),
        })

    return pd.DataFrame(roster_records), shift_counts

if st.button("🚀 Generate Roster & View Stats"):
    df_roster, stats_dict = generate_roster()
    
    # 1. Main Roster View
    st.subheader("Current Roster")
    st.table(df_roster)
    
    st.divider()
    
    # 2. Stats View
    st.subheader("📊 Workload Statistics")
    col1, col2 = st.columns([1, 2])
    
    stats_df = pd.DataFrame(list(stats_dict.items()), columns=["Staff Member", "Total Shifts"])
    stats_df = stats_df.sort_values(by="Total Shifts", ascending=False)
    
    with col1:
        st.write("Shift Breakdown per Member")
        st.dataframe(stats_df, hide_index=True)
    
    with col2:
        st.bar_chart(stats_df.set_index("Staff Member"))
    
    # Download
    csv = df_roster.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Spreadsheet", csv, "team_roster_with_stats.csv", "text/csv")