import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. DATA & CONFIGURATION ---
# Fixed General Shift (G) - Mon-Fri only
fixed_general = ["Durgeshkumar Singh (TL)", "Ranjit Kumar S P (L3)", "Athira Pillai (L2)"]

# Balanced Rotating Groups (5 members each where possible)
groups = {
    'Group 1': ["Mahesh Arokia (TL)", "Ashish Chaturvedi (L3)", "Arsalan Shaikh (L2)", "Sarika Gadekar (L2)", "Abhijeet Gorivale (L2)"],
    'Group 2': ["Rajkumar Chitravelu (TL)", "Arjun Ghadi (L3)", "Akash Sahu (L2)", "Mahadev Bhusnar (L2)", "Mehmood Nachan (L2)"],
    'Group 3': ["Mehul Dholakiya (TL)", "Vigneshwaran Prakash (TL)", "Sanjiv Sudhakar (L3)", "Gandharv Adhikari (L2)", "Manoj Khatri (L2)"],
    'Group 4': ["Atul Dhamal (TL)", "Varad C N (L3)", "Pranav Markande (L2)", "Mahesh Pawar (L2)", "Nitin Gadekar (L2)"],
    'Group 5': ["Paras Shah (TL)", "Fernando Gerard (L2)", "Abhijeet Gorivale (L2)", "Akash Sahu (L2)", "Pranav Markande (L2)"] 
}

# --- 2. ROSTER GENERATION ---
def generate_balanced_roster(start_date, duration):
    # Pattern: 5M, 2O, 5A, 3O, 5N, 5O = 25 days total
    # Total Working Days in 25 days = 15
    shift_pattern = (['M']*5 + ['O']*2 + ['A']*5 + ['O']*3 + ['N']*5 + ['O']*5)
    
    roster_rows = []
    all_staff = list(set(fixed_general + [e for g in groups.values() for e in g]))
    
    for d in range(duration):
        curr_date = start_date + timedelta(days=d)
        is_weekend = curr_date.weekday() >= 5 # Sat/Sun
        day_data = {'Date': curr_date.strftime('%Y-%m-%d'), 'Day': curr_date.strftime('%A')}
        
        # General Shift Assignment
        for emp in fixed_general:
            day_data[emp] = 'OFF' if is_weekend else 'G'
            
        # Rotating Shift Assignment
        for i, (g_name, members) in enumerate(groups.items()):
            # Staggering ensures different groups cover M, A, and N simultaneously
            shift = shift_pattern[(d + i * 5) % 25]
            for m in members:
                # If it's a weekend and they aren't on a working shift, mark as OFF
                if is_weekend and shift == 'O':
                    day_data[m] = 'OFF'
                else:
                    day_data[m] = shift
        
        roster_rows.append(day_data)
    return roster_rows, all_staff

# --- 3. STATS & EQUALITY VALIDATOR ---
def get_stats(roster_rows, all_staff, start_date, duration):
    # Calculate Total Saturdays and Sundays in the period
    total_weekends = sum(1 for d in range(duration) if (start_date + timedelta(days=d)).weekday() >= 5)
    
    summary = []
    for emp in all_staff:
        emp_shifts = [row.get(emp, 'O') for row in roster_rows]
        
        working_days = sum(1 for s in emp_shifts if s in ['M', 'A', 'N', 'G'])
        
        # Weekoff is counted if it's a Sat/Sun and they didn't work
        weekoffs = 0
        for d in range(duration):
            curr_date = start_date + timedelta(days=d)
            if curr_date.weekday() >= 5 and emp_shifts[d] in ['O', 'OFF']:
                weekoffs += 1
                
        summary.append({
            'Employee': emp,
            'Working Days': working_days,
            'Actual Weekoffs': weekoffs,
            'Target Weekoffs': total_weekends,
            'Equality Status': '✅ Balanced' if weekoffs == total_weekends else '⚠️ Adjusted'
        })
    return pd.DataFrame(summary)

# --- 4. STREAMLIT UI ---
st.title("⚖️ Balanced Team Roster")
st.sidebar.header("Controls")
s_date = st.sidebar.date_input("Start Date", datetime(2026, 3, 1))
days = st.sidebar.slider("Days", 7, 31, 31)

rows, staff = generate_balanced_roster(s_date, days)
stats_df = get_stats(rows, staff, s_date, days)

t1, t2 = st.tabs(["Roster View", "Equality Stats"])
with t1:
    st.dataframe(pd.DataFrame(rows))
with t2:
    st.subheader("Working Days & Weekoff Equality")
    st.write(f"**Total Saturdays/Sundays in this month:** {stats_df['Target Weekoffs'].iloc[0]}")
    st.table(stats_df)