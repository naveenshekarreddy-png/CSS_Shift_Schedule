import streamlit as st
import pandas as pd

# ... [Keep previous logic for generating roster_rows and daily_stats] ...

# --- COVERAGE VALIDATOR LOGIC ---
st.sidebar.header("Validation Rules")
min_staff_required = st.sidebar.number_input("Min Staff per Shift", value=5)

def highlight_understaffed(val):
    """Highlights cells red if staff count is below the minimum required."""
    color = '#ff9999' if isinstance(val, int) and val < min_staff_required else ''
    return f'background-color: {color}'

# --- UPDATED DISPLAY SECTION ---
with tab2:
    st.subheader("Daily Shift Availability & Validator")
    
    # Create the stats dataframe
    stats_df = pd.DataFrame(daily_stats)
    
    # Validation Logic: Check if any shift is understaffed
    understaffed_days = stats_df[
        (stats_df['Morning'] < min_staff_required) | 
        (stats_df['Afternoon'] < min_staff_required) | 
        (stats_df['Night'] < min_staff_required)
    ]
    
    if not understaffed_days.empty:
        st.error(f"⚠️ Critical Alert: Coverage falls below {min_staff_required} on {len(understaffed_days)} days!")
        st.warning("Check 'Total on Leave' to see if high absence is the cause.")
    else:
        st.success(f"✅ Coverage Check Passed: All shifts have at least {min_staff_required} members.")

    # Display Table with Conditional Formatting
    st.write("### Coverage Heatmap")
    st.dataframe(
        stats_df.style.applymap(
            highlight_understaffed, 
            subset=['Morning', 'Afternoon', 'Night']
        )
    )

    # Visualizing the gaps
    st.line_chart(stats_df.set_index('Date')[['Morning', 'Afternoon', 'Night']])