import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. AUTHENTICATION SYSTEM ---
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] == "admin" and st.session_state["password"] == "roster2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username and password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

# --- 2. MAIN APP LOGIC (Only runs if authenticated) ---
if check_password():
    st.set_page_config(page_title="Team Roster Tool", layout="wide")
    st.sidebar.success("Logged In Successfully")
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    st.title("📅 Rotational Shift Roster Tool")

    # --- 3. DATA & CONFIGURATION ---
    fixed_general = ["Durgeshkumar Singh (TL)", "Ranjit Kumar S P (L3)", "Athira Pillai (L2)"]
    l3_backups = ["Manoj Khatri (L2)", "Mehmood Nachan (L2)", "Nitin Gadekar (L2)", "Mahesh Pawar (L2)"]

    groups = {
        'Group 1': ["Mahesh Arokia (TL)", "Ashish Chaturvedi (L3)", "Arsalan Shaikh (L2)", "Sarika Gadekar (L2)", "Abhijeet Gorivale (L2)"],
        'Group 2': ["Rajkumar Chitravelu (TL)", "Arjun Ghadi (L3)", "Akash Sahu (L2)", "Mahadev Bhusnar (L2)", "Mehmood Nachan (L2)"],
        'Group 3': ["Mehul Dholakiya (TL)", "Vigneshwaran Prakash (TL)", "Sanjiv Sudhakar (L3)", "Gandharv Adhikari (L2)", "Manoj Khatri (L2)"],
        'Group 4': ["Atul Dhamal (TL)", "Varad C N (L3)", "Pranav Markande (L2)", "Mahesh Pawar (L2)", "Nitin Gadekar (L2)"],
        'Group 5': ["Paras Shah (TL)", "Fernando Gerard (L2)", "Abhijeet Gorivale (L2)"] 
    }

    # Sidebar Roster Settings
    st.sidebar.header("Roster Settings")
    start_date = st.sidebar.date_input("Start Date", datetime(2026, 3, 1))
    duration = st.sidebar.slider("Number of Days", 7, 62, 31)
    min_staff = st.sidebar.number_input("Min Staff per Shift", value=5)

    # Roster Generation
    shift_pattern = (['M']*5 + ['O']*2 + ['A']*5 + ['O']*3 + ['N']*5 + ['O']*5)
    all_staff = list(set(fixed_general + [e for g in groups.values() for e in g]))
    roster_rows = []
    hours = {name: 0 for name in all_staff}

    for d in range(duration):
        curr_date = start_date + timedelta(days=d)
        date_str = curr_date.strftime('%Y-%m-%d')
        is_weekend = curr_date.weekday() >= 5
        day_data = {'Date': date_str, 'Day': curr_date.strftime('%A')}
        
        current_day = {emp: ('OFF' if is_weekend else 'G') for emp in fixed_general}
        
        for i, (g_name, members) in enumerate(groups.items()):
            shift = shift_pattern[(d + i * 5) % 25]
            for m in members:
                current_day[m] = shift
        
        for emp, shft in current_day.items():
            if any(s in shft for s in ['M', 'A', 'N', 'G']): hours[emp] += 8
        
        day_data.update(current_day)
        roster_rows.append(day_data)

    df = pd.DataFrame(roster_rows)

    # Tabs for Display
    tab1, tab2, tab3 = st.tabs(["📅 Live Roster", "📊 Daily Coverage Stats", "👤 Employee Summary"])

    with tab1:
        st.subheader("Monthly Roster View")
        st.dataframe(df)

    with tab2:
        st.subheader("Daily Shift Availability")
        daily_stats = []
        for row in roster_rows:
            shifts = list(row.values())
            daily_stats.append({
                'Date': row['Date'],
                'Morning': sum(1 for s in shifts if 'M' in str(s)),
                'Afternoon': sum(1 for s in shifts if 'A' in str(s)),
                'Night': sum(1 for s in shifts if 'N' in str(s)),
            })
        stats_df = pd.DataFrame(daily_stats)
        st.dataframe(stats_df.style.applymap(lambda x: 'background-color: #ff9999' if isinstance(x, int) and x < min_staff else '', subset=['Morning', 'Afternoon', 'Night']))

    with tab3:
        st.subheader("Employee Work Summary")
        summary_data = []
        for emp in all_staff:
            emp_shifts = [row.get(emp, 'O') for row in roster_rows]
            working = sum(1 for s in emp_shifts if any(x in str(s) for x in ['M', 'A', 'N', 'G']))
            weekoffs = sum(1 for i, s in enumerate(emp_shifts) if (start_date + timedelta(days=i)).weekday() >= 5 and s in ['O', 'OFF'])
            summary_data.append({'Employee': emp, 'Working Days': working, 'Weekoffs (Sat/Sun)': weekoffs, 'Total Hours': hours[emp]})
        st.dataframe(pd.DataFrame(summary_data))