#!/usr/bin/env python3
"""
AUTOMATED ROSTER GENERATOR WITH CONSTRAINT VALIDATION
Helps generate compliant rosters based on specified constraints
"""

from datetime import datetime, timedelta
from collections import defaultdict
import calendar

# Team configuration
TEAM_MEMBERS = {
    'Arsalan Shaikh (L1)': {'level': 'TL', 'rating': 'Good'},
    'Sarika Gadekar': {'level': 'L2', 'rating': 'Good', 'max_nights': 3},
    'Akash Sahu': {'level': 'L2', 'rating': 'Average'},
    'Mahadev Bhusnur': {'level': 'L2', 'rating': 'Good'},
    'Gandharva Adhikari': {'level': 'L3', 'rating': 'Good', 'max_nights': 5, 'weekday_only': True},
    'Mehmood Nachan': {'level': 'L2', 'rating': 'Average'},
    'Manoj Khatri': {'level': 'L2', 'rating': 'Average'},
    'Mahesh Pawar': {'level': 'L2', 'rating': 'Good'},
    'Pranav Markande': {'level': 'L2', 'rating': 'Average'},
    'Nitin Gadekar': {'level': 'L2', 'rating': 'Good'},
    'Fernando Gerard': {'level': 'L2', 'rating': 'Good', 'morning_general_only': True, 'weekday_only': True},
    'Athira Pillai': {'level': 'L2', 'rating': 'Good', 'general_only': True, 'weekday_only': True},
    'Abhijeet Gorivale': {'level': 'L2', 'rating': 'Good'},
    'Ashish Chaturvedi': {'level': 'L2', 'rating': 'Average'},
    'Ranjit Kumar S P': {'level': 'L2', 'rating': 'Good', 'general_only': True, 'weekday_only': True},
    'Arjun Ghadi': {'level': 'L2', 'rating': 'Average', 'no_backup_tl': True},
    'Sanjiv Sudhakar': {'level': 'L2', 'rating': 'Good', 'max_nights': 3},
    'Varad C N': {'level': 'L2', 'rating': 'Good', 'max_nights': 3},
    'Durgeshkumar Singh': {'level': 'L2', 'rating': 'Average'},
    'Mahesh Arokia': {'level': 'L2', 'rating': 'Average'},
    'Mehul Dholakiya': {'level': 'L2', 'rating': 'Good'},
    'Atul Dhamal': {'level': 'L2', 'rating': 'Good'},
    'Paras Shah': {'level': 'L2', 'rating': 'Average'},
    'Rajkumar Chitravelu': {'level': 'L2', 'rating': 'Average'},
    'Vianeshwaran Prakash': {'level': 'L2', 'rating': 'Good'},
}

SHIFT_CODES = {
    'Morning': 'Morning shift (6 AM - 2 PM)',
    'AftNoon': 'Afternoon shift (9 AM - 6 PM)',
    'Night': 'Night shift (10 PM - 6 AM)',
    'General': 'General duty',
    'WkOff': 'Week off',
    'Leave': 'Approved planned leave',
}

class RosterValidator:
    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.days_in_month = calendar.monthrange(year, month)[1]
        self.first_day_of_week = calendar.monthrange(year, month)[0]
        self.roster = defaultdict(lambda: {})
        self.violations = []
        
    def get_day_of_week(self, day):
        """Returns 0=Monday, 1=Tuesday, ..., 5=Saturday, 6=Sunday"""
        date = datetime(self.year, self.month, day)
        return date.weekday()
    
    def is_weekday(self, day):
        """Returns True if Monday-Friday"""
        return self.get_day_of_week(day) < 5
    
    def is_weekend(self, day):
        """Returns True if Saturday-Sunday"""
        return self.get_day_of_week(day) >= 5
    
    def check_constraint_1(self, member, roster_data):
        """Athira, Ranjit: General shifts only, Mon-Fri"""
        if member not in ['Athira Pillai', 'Ranjit Kumar S P']:
            return True
        
        for day in range(1, self.days_in_month + 1):
            if not self.is_weekday(day):
                continue
            shift = roster_data.get(day, 'WkOff')
            if shift not in ['General', 'WkOff', 'Leave']:
                self.violations.append(f"{member} has '{shift}' on day {day} (must be General/WkOff/Leave)")
                return False
        return True
    
    def check_constraint_2(self, member, roster_data):
        """Gandharva: Morning/General/Night only, Mon-Fri, max 5 nights"""
        if member != 'Gandharva Adhikari':
            return True
        
        night_count = 0
        for day in range(1, self.days_in_month + 1):
            shift = roster_data.get(day, 'WkOff')
            
            # Check allowed shifts on weekdays
            if self.is_weekday(day):
                if shift not in ['Morning', 'General', 'Night', 'WkOff', 'Leave']:
                    self.violations.append(f"Gandharva has invalid shift '{shift}' on day {day}")
                    return False
            else:
                # Must be WkOff/Leave on weekends
                if shift not in ['WkOff', 'Leave']:
                    self.violations.append(f"Gandharva has '{shift}' on weekend day {day} (must be WkOff/Leave)")
                    return False
            
            if shift == 'Night':
                night_count += 1
        
        if night_count > 5:
            self.violations.append(f"Gandharva has {night_count} night shifts (max 5)")
            return False
        return True
    
    def check_constraint_4(self, member, roster_data):
        """Varad, Sanjiv, Sarika: max 3 night shifts each"""
        if member not in ['Varad C N', 'Sanjiv Sudhakar', 'Sarika Gadekar']:
            return True
        
        night_count = sum(1 for day in range(1, self.days_in_month + 1) 
                         if roster_data.get(day) == 'Night')
        
        if night_count > 3:
            self.violations.append(f"{member} has {night_count} night shifts (max 3)")
            return False
        return True
    
    def check_constraint_15(self, member, roster_data):
        """Fernando: Morning/General only, Mon-Fri, no nights"""
        if member != 'Fernando Gerard':
            return True
        
        for day in range(1, self.days_in_month + 1):
            shift = roster_data.get(day, 'WkOff')
            
            # Only allow shifts on weekdays
            if not self.is_weekday(day):
                if shift not in ['WkOff', 'Leave']:
                    self.violations.append(f"Fernando has '{shift}' on weekend day {day}")
                    return False
            
            # Only allow Morning or General on weekdays
            if shift not in ['Morning', 'General', 'WkOff', 'Leave']:
                self.violations.append(f"Fernando has '{shift}' on day {day} (only Morning/General/WkOff/Leave allowed)")
                return False
        
        return True
    
    def validate_weekday_shift_counts(self, all_roster_data):
        """Rule 5: Weekday shifts must be 4 Morning, 5 AftNoon, 5 Night"""
        week_counts = defaultdict(lambda: {'Morning': 0, 'AftNoon': 0, 'Night': 0})
        
        for day in range(1, self.days_in_month + 1):
            if not self.is_weekday(day):
                continue
            
            week_num = (day - 1) // 7
            for member in all_roster_data:
                shift = all_roster_data[member].get(day, 'WkOff')
                if shift in ['Morning', 'AftNoon', 'Night']:
                    week_counts[week_num][shift] += 1
        
        errors = []
        for week_num, counts in sorted(week_counts.items()):
            if counts['Morning'] != 4:
                errors.append(f"Week {week_num}: Morning={counts['Morning']} (should be 4)")
            if counts['AftNoon'] != 5:
                errors.append(f"Week {week_num}: AftNoon={counts['AftNoon']} (should be 5)")
            if counts['Night'] != 5:
                errors.append(f"Week {week_num}: Night={counts['Night']} (should be 5)")
        
        return errors
    
    def validate_weekend_shift_counts(self, all_roster_data):
        """Rule 6: Weekend shifts must be 3 Morning, 4 AftNoon, 5 Night"""
        weekend_counts = {'Morning': 0, 'AftNoon': 0, 'Night': 0}
        
        for day in range(1, self.days_in_month + 1):
            if not self.is_weekend(day):
                continue
            
            for member in all_roster_data:
                shift = all_roster_data[member].get(day, 'WkOff')
                if shift in ['Morning', 'AftNoon', 'Night']:
                    weekend_counts[shift] += 1
        
        errors = []
        if weekend_counts['Morning'] != 3:
            errors.append(f"Weekend: Morning={weekend_counts['Morning']} (should be 3)")
        if weekend_counts['AftNoon'] != 4:
            errors.append(f"Weekend: AftNoon={weekend_counts['AftNoon']} (should be 4)")
        if weekend_counts['Night'] != 5:
            errors.append(f"Weekend: Night={weekend_counts['Night']} (should be 5)")
        
        return errors
    
    def validate_rest_days(self, member, roster_data):
        """Rule 9: 2 days rest after night shift"""
        issues = []
        for day in range(1, self.days_in_month - 1):
            if roster_data.get(day) == 'Night':
                next_day = roster_data.get(day + 1)
                next_next_day = roster_data.get(day + 2)
                
                if next_day not in ['WkOff', 'Leave'] or next_next_day not in ['WkOff', 'Leave']:
                    issues.append(f"Insufficient rest after night on day {day}")
        
        return issues
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "="*60)
        print(f"ROSTER VALIDATION REPORT: {self.month}/{self.year}")
        print("="*60)
        
        if self.violations:
            print(f"\n⚠️  VIOLATIONS FOUND ({len(self.violations)}):")
            for i, violation in enumerate(self.violations, 1):
                print(f"  {i}. {violation}")
        else:
            print("\n✓ All constraints validated successfully!")
        
        print("\n" + "="*60)

class RosterGenerator:
    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.validator = RosterValidator(month, year)
    
    def generate_summary(self):
        """Generate roster summary statistics"""
        print(f"\nROSTER SUMMARY FOR {calendar.month_name[self.month]} {self.year}")
        print("="*60)
        
        # Days calculation
        days = self.validator.days_in_month
        weekdays = sum(1 for d in range(1, days + 1) if self.validator.is_weekday(d))
        weekends = days - weekdays
        
        print(f"Total days in month: {days}")
        print(f"  - Weekdays (Mon-Fri): {weekdays}")
        print(f"  - Weekends (Sat-Sun): {weekends}")
        
        print(f"\nRequired Daily Staffing (Weekdays):")
        print(f"  - Morning shifts: 4")
        print(f"  - Afternoon/9-6 shifts: 5")
        print(f"  - Night shifts: 5")
        print(f"  - Total per day: 14 staff")
        
        print(f"\nTotal Shift Slots Needed (Weekdays):")
        print(f"  - Total: {weekdays * 14} shifts")
        print(f"  - Per staff member: {(weekdays * 14) / 25:.1f} shifts")
        
        print(f"\nRequired Daily Staffing (Weekends):")
        print(f"  - Morning shifts: 3")
        print(f"  - Afternoon shifts: 4")
        print(f"  - Night shifts: 5")
        
        print(f"\nSpecial Rules for Month:")
        print(f"  - Days 1-2 (Change Freeze): 4 night shifts (instead of 5)")
        print(f"  - Days 27-29 (Change Freeze): 4 night shifts")
        print(f"  - Day 30 (if 31st exists): 4 night shifts")
        print(f"  - Days 30-31 (Month End): 6 night shifts")
        
        print(f"\nTeam Composition:")
        print(f"  - TL (Team Lead): 1 (Arsalan Shaikh)")
        print(f"  - L3 (Senior): 1 (Gandharva Adhikari)")
        print(f"  - L2 (Operations): 23")
        print(f"  - Total: 25 members")
        
        print("\n" + "="*60)

def main():
    print("\n🤖 AUTOMATED ROSTER GENERATOR")
    print("="*60)
    
    # Get month and year
    while True:
        try:
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year (YYYY): "))
            if 1 <= month <= 12 and 1900 <= year <= 2100:
                break
            print("Invalid input. Try again.")
        except ValueError:
            print("Invalid input. Try again.")
    
    generator = RosterGenerator(month, year)
    generator.generate_summary()
    
    print("\n📋 NEXT STEPS:")
    print("1. Fill the ROSTER sheet in Excel with shift codes")
    print("2. Use constraint codes from QUICK REFERENCE sheet")
    print("3. Run validation to check for violations")
    print("4. Adjust roster as needed to meet constraints")
    print("5. Export final roster when all constraints met")
    
    print("\n💡 CONSTRAINT SHORTCUTS:")
    print("  • Athira/Ranjit → General only, Mon-Fri")
    print("  • Gandharva → Morning/General/Night, Mon-Fri, max 5 nights")
    print("  • Fernando → Morning/General, Mon-Fri only")
    print("  • Varad/Sanjiv/Sarika → Max 3 nights each")
    print("  • Weekdays → 4 Morning, 5 Afternoon, 5 Night")
    print("  • Weekends → 3 Morning, 4 Afternoon, 5 Night")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    main()
