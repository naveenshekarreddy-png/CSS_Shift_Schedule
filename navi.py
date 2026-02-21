import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Team Roster Tool", layout="wide")
st.title("📅 Rotational Shift Roster Tool")

# --- DATA SETUP ---
fixed_general = ["Durgeshkumar Singh (TL)", "Ranjit Kumar S P (L3)", "Athira Pillai (L2)"]
l3_backups = ["Manoj Khatri (L2)", "Mehmood Nachan (L2)", "Nitin Gadekar (L2)", "Mahesh Pawar (L2)"]

groups = {
    'Group 1': ["Mahesh Arokia (TL)", "Ashish Chaturvedi (L3)", "Arsalan Shaikh (L2)", "Sarika Gadekar (L2)", "Abhijeet Gorivale (L2)"],
    'Group 2': ["Rajkumar Chitravelu (TL)", "Arjun Ghadi (L3)", "Akash Sahu (L2)", "Mahadev Bhusnar (L2)", "Mehmood Nachan (L2)"],
    'Group 3': ["Mehul Dholakiya (TL)", "Vigneshwaran Prakash (TL)", "Sanjiv Sudhakar (L3)", "Gandharv Adhikari (L2)", "Manoj Khatri (L2)"],
    'Group 4': ["Atul Dhamal (TL)", "Varad C N (L3)", "Pranav Markande (L2)", "Mahesh Pawar (L2)", "Nitin Gadekar (L2)"],
    'Group 5': ["Paras Shah (TL)", "Fernando Gerard (L2)", "Akash Sahu (L2)"] 
}

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Roster Settings")
start_date = st.sidebar.date_input("Start Date", datetime(2026, 3, 1))
duration = st.sidebar.slider("Number of Days", 7, 60, 31)

# Leave Entry System
st.sidebar.subheader("Log Leave")
leaver = st.sidebar.selectbox("Select Employee", [e for g in groups.values() for e in g] + fixed_general)
leave_date = st.sidebar.date_input("Leave Date", start_date)
if st.sidebar.button("Add Leave"):
    if 'leaves' not in st.session_state: st.session_state.leaves = {}
    date_key = leave_date.strftime('%Y-%m-%d')
    st.session_state.leaves.setdefault(date_key, []).append(leaver)
    st.sidebar.success(f"Added leave for {leaver}")

# --- ROSTER LOGIC ---
shift_pattern = (['M']*5 + ['O']*2 + ['A']*5 + ['O']*3 + ['N']*5 + ['O']*5)
all_staff = list(set(fixed_general + [e for g in groups.values() for e in g]))
hours = {name: 0 for name in all_staff}
roster_rows = []

for d in range(duration):
    curr_date = start_date + timedelta(days=d)
    date_str = curr_date.strftime('%Y-%m-%d')
    is_weekend = curr_date.weekday() >= 5
    day_data = {'Date': date_str, 'Day': curr_date.strftime('%A')}
    
    current_day = {emp: ('OFF' if is_weekend else 'G') for emp in fixed_general}
    off_pool = []
    for i, (g_name, members) in enumerate(groups.items()):
        shift = shift_pattern[(d + i * 5) % 25]
        for m in members:
            current_day[m] = shift
            if shift == 'O': off_pool.append(m)

    # Process Leaves & Subs
    day_leaves = st.session_state.get('leaves', {}).get(date_str, [])
    for l_person in day_leaves:
        orig = current_day.get(l_person)
        if orig and orig not in ['O', 'OFF']:
            role = 'L3' if '(L3)' in l_person else 'TL' if '(TL)' in l_person else 'L2'
            sub = next((s for s in off_pool if f'({role})' in s), None)
            if not sub and role == 'L3':
                sub = next((s for s in off_pool if any(b in s for b in l3_backups)), None)
            if sub:
                current_day[sub] = f"{orig} (SUB)"
                off_pool.remove(sub)
            current_day[l_person] = 'LEAVE'

    # Track Hours
    for emp, shft in current_day.items():
        if any(s in shft for s in ['M', 'A', 'N', 'G']): hours[emp] += 8
    
    day_data.update(current_day)
    roster_rows.append(day_data)

# --- DISPLAY ---
df = pd.DataFrame(roster_rows)
st.subheader("Current Roster")
st.dataframe(df.style.applymap(lambda x: 'background-color: #ffcccc' if x == 'LEAVE' else ('background-color: #ccffcc' if '(SUB)' in str(x) else '')))

st.subheader("Work Hour Summary")
st.table(pd.DataFrame(list(hours.items()), columns=['Employee', 'Total Hours']))

# Download Button
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Roster as CSV", data=csv, file_name="roster.csv", mime="text/csv")