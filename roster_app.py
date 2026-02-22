from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import json
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# In-memory user database (replace with real DB in production)
USERS_DB = {
    "manager@roster.com": {"password": "manager123", "role": "manager", "name": "Manager"},
    "hr@roster.com": {"password": "hr123", "role": "hr", "name": "HR"},
    "admin@roster.com": {"password": "admin123", "role": "admin", "name": "Admin"},
}

# Team member database
TEAM_DATA = {
    "TLs": [
        "Durgeshkumar Singh",
        "Mahesh Arokia",
        "Mehul Dholakiya",
        "Atul Dhamal",
        "Paras Shah",
        "Rajkumar Chitravelu",
        "Vigneshwaran Prakash",
    ],
    "L3s": [
        "Ashish Chaturvedi",
        "Ranjit Kumar S P",
        "Arjun Ghadi",
        "Sanjiv Sudhakar",
        "Varad C N",
    ],
    "L2s": [
        "Arsalan Shaikh",
        "Akash Sahu",
        "Mahadev Bhusnar",
        "Gandharv Adhikari",
        "Mehmood Nachan",
        "Manoj Khatri",
        "Mahesh Pawar",
        "Pranav Markande",
        "Nitin Gadekar",
        "Fernando Gerard",
        "Athira Pillai",
        "Abhijeet Gorivale",
    ],
}

CONSTRAINTS = {
    "Athira Pillai": {"shifts": ["General"], "workdays": "Mon-Fri"},
    "Ranjit Kumar S P": {"shifts": ["General"], "workdays": "Mon-Fri"},
    "Gandharv Adhikari": {"excludeShifts": ["Afternoon"], "workdays": "Mon-Fri"},
    "Fernando Gerard": {"shifts": ["Morning", "General"], "workdays": "Mon-Fri"},
    "Varad C N": {"maxNights": 3, "preferredShifts": ["General", "Morning", "Afternoon"]},
    "Sanjiv Sudhakar": {"maxNights": 3, "preferredShifts": ["General", "Morning", "Afternoon"]},
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = USERS_DB.get(email)
        if user and user['password'] == password:
            session['user'] = email
            session['role'] = user['role']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid email or password")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if email in USERS_DB:
            return render_template('register.html', error="Email already registered")
        
        USERS_DB[email] = {
            "password": password,
            "role": "viewer",
            "name": name
        }
        session['user'] = email
        session['role'] = "viewer"
        session['name'] = name
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user_name=session.get('name'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/generate-roster', methods=['POST'])
@login_required
def generate_roster():
    data = request.json
    month_year = data.get('monthYear')
    
    try:
        year, month = map(int, month_year.split('-'))
        days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31
    except:
        return jsonify({'error': 'Invalid month format'}), 400
    
    all_members = TEAM_DATA['TLs'] + TEAM_DATA['L3s'] + TEAM_DATA['L2s']
    roster = {}
    member_night_counts = {}
    
    for member in all_members:
        roster[member] = {}
        member_night_counts[member] = 0
    
    # Generate roster for each day
    for day in range(1, days_in_month + 1):
        date = datetime(year, month, day)
        is_weekend = date.weekday() >= 4  # Saturday=4, Sunday=5
        is_freeze = day in [1, 2, 27, 28, 29]
        is_month_end = day == days_in_month
        
        # Determine shift requirements
        if is_weekend:
            shift_reqs = {"Morning": 3, "Afternoon": 4, "Night": 5}
        elif is_freeze:
            shift_reqs = {"Morning": 4, "Afternoon": 4, "Night": 4, "General": 5}
        elif is_month_end:
            shift_reqs = {"Morning": 4, "Afternoon": 4, "Night": 6, "General": 4}
        else:
            shift_reqs = {"Morning": 4, "Afternoon": 4, "Night": 5, "General": 5}
        
        day_assignments = {}
        assigned = set()
        
        # Priority 1: Assign TLs
        for i, shift_type in enumerate(shift_reqs.keys()):
            tl = TEAM_DATA['TLs'][i % len(TEAM_DATA['TLs'])]
            if shift_type not in day_assignments:
                day_assignments[shift_type] = []
            day_assignments[shift_type].append(tl)
            assigned.add(tl)
        
        # Priority 2: Assign L3s
        for l3 in TEAM_DATA['L3s']:
            if l3 in assigned:
                continue
            
            constraint = CONSTRAINTS.get(l3, {})
            if constraint.get('maxNights') and member_night_counts[l3] >= constraint['maxNights'] and not is_month_end:
                continue
            
            available_shifts = [s for s in shift_reqs if shift_reqs[s] > 0 and s not in day_assignments]
            
            if available_shifts:
                shift_type = available_shifts[0]
                if shift_type not in day_assignments:
                    day_assignments[shift_type] = []
                day_assignments[shift_type].append(l3)
                assigned.add(l3)
                shift_reqs[shift_type] -= 1
                if shift_type == "Night":
                    member_night_counts[l3] += 1
        
        # Priority 3: Assign L2s
        for l2 in TEAM_DATA['L2s']:
            if l2 in assigned:
                continue
            
            constraint = CONSTRAINTS.get(l2, {})
            if constraint.get('workdays') == 'Mon-Fri' and is_weekend:
                continue
            
            available_shifts = []
            for shift_type in shift_reqs:
                if shift_reqs[shift_type] > 0:
                    if constraint.get('shifts'):
                        if shift_type in constraint['shifts']:
                            available_shifts.append(shift_type)
                    elif constraint.get('excludeShifts'):
                        if shift_type not in constraint['excludeShifts']:
                            available_shifts.append(shift_type)
                    else:
                        available_shifts.append(shift_type)
            
            if available_shifts:
                shift_type = available_shifts[0]
                if shift_type not in day_assignments:
                    day_assignments[shift_type] = []
                day_assignments[shift_type].append(l2)
                assigned.add(l2)
                shift_reqs[shift_type] -= 1
                if shift_type == "Night":
                    member_night_counts[l2] += 1
        
        # Assign remaining to General or Off
        for member in all_members:
            if member not in assigned:
                if not is_weekend and shift_reqs.get('General', 0) > 0:
                    if 'General' not in day_assignments:
                        day_assignments['General'] = []
                    day_assignments['General'].append(member)
                    assigned.add(member)
                    shift_reqs['General'] -= 1
        
        # Assign remaining as Off
        for member in all_members:
            if member not in assigned:
                roster[member][day] = 'WkOff' if is_weekend else 'Off'
        
        # Record assignments
        for shift_type, members in day_assignments.items():
            for member in members:
                roster[member][day] = shift_type
    
    return jsonify({
        'success': True,
        'roster': roster,
        'daysInMonth': days_in_month,
        'totalMembers': len(all_members),
        'nightShifts': sum(member_night_counts.values())
    })

@app.route('/api/export-csv', methods=['POST'])
@login_required
def export_csv():
    data = request.json
    roster = data.get('roster')
    month_year = data.get('monthYear')
    
    try:
        year, month = map(int, month_year.split('-'))
        days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31
    except:
        return jsonify({'error': 'Invalid month format'}), 400
    
    all_members = TEAM_DATA['TLs'] + TEAM_DATA['L3s'] + TEAM_DATA['L2s']
    
    csv_content = "Member Name,Role,"
    for day in range(1, days_in_month + 1):
        date = datetime(year, month, day)
        day_name = date.strftime('%a')
        csv_content += f"{day}-{day_name},"
    csv_content += "Total Nights\n"
    
    for member in all_members:
        role = "TL" if member in TEAM_DATA['TLs'] else "L3" if member in TEAM_DATA['L3s'] else "L2"
        csv_content += f"{member},{role},"
        
        night_count = 0
        for day in range(1, days_in_month + 1):
            shift = roster.get(member, {}).get(str(day), 'Off')
            csv_content += f"{shift},"
            if shift == "Night":
                night_count += 1
        csv_content += f"{night_count}\n"
    
    return jsonify({
        'success': True,
        'csv': csv_content,
        'filename': f"roster_{month_year}.csv"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
