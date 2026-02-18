<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oracle CSS DBA Team Shift Schedule</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }

        header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }

        header h1 {
            margin-bottom: 10px;
        }

        .controls {
            display: flex;
            justify-content: space-between;
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #ddd;
            flex-wrap: wrap;
        }

        .button-group button {
            padding: 10px 20px;
            margin: 0 5px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }

        .btn-primary {
            background: #3498db;
            color: white;
        }

        .btn-success {
            background: #27ae60;
            color: white;
        }

        .btn-danger {
            background: #e74c3c;
            color: white;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .team-management, .roster-controls {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .panel {
            padding: 20px;
            margin: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #ddd;
        }

        .team-panel {
            flex: 1;
            min-width: 300px;
        }

        .settings-panel {
            flex: 1;
            min-width: 300px;
        }

        input, select {
            width: 100%;
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .team-list {
            margin-top: 10px;
            max-height: 300px;
            overflow-y: auto;
        }

        .team-member {
            display: flex;
            justify-content: space-between;
            padding: 8px;
            margin: 5px 0;
            background: white;
            border-radius: 4px;
            border: 1px solid #ddd;
        }

        .agent-stats {
            font-size: 12px;
            color: #666;
        }

        .roster-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 14px;
        }

        .roster-table th {
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: center;
            position: sticky;
            top: 0;
        }

        .roster-table td {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: center;
            vertical-align: top;
        }

        .shift-morning {
            background-color: #e8f6f3;
        }

        .shift-afternoon {
            background-color: #fef9e7;
        }

        .shift-night {
            background-color: #fbeeee;
        }

        .day-off {
            background-color: #f5f5f5;
            color: #999;
            font-style: italic;
        }

        .agent-tl {
            background: #e74c3c;
            color: white;
            padding: 3px 6px;
            border-radius: 3px;
            margin: 1px;
            display: inline-block;
            font-size: 11px;
        }

        .agent-l3 {
            background: #3498db;
            color: white;
            padding: 3px 6px;
            border-radius: 3px;
            margin: 1px;
            display: inline-block;
            font-size: 11px;
        }

        .agent-l2 {
            background: #27ae60;
            color: white;
            padding: 3px 6px;
            border-radius: 3px;
            margin: 1px;
            display: inline-block;
            font-size: 11px;
        }

        footer {
            text-align: center;
            padding: 20px;
            background: #ecf0f1;
            color: #7f8c8d;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px;
            background: #27ae60;
            color: white;
            border-radius: 5px;
            display: none;
            z-index: 1000;
        }

        .stats-panel {
            background: #2c3e50;
            color: white;
            padding: 15px;
            margin: 10px;
            border-radius: 5px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }

        .stat-item {
            text-align: center;
        }

        .stat-value {
            font-size: 24px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="notification" id="notification">Operation completed successfully!</div>

    <div class="container">
        <header>
            <h1>Oracle CSS DBA Team Shift Schedule</h1>
            <p>Team: 24 Members | Shifts: Morning, Afternoon, Night</p>
        </header>

        <div class="stats-panel">
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value" id="totalTL">7</div>
                    <div>Team Leads</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="totalL3">5</div>
                    <div>L3 Support</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="totalL2">12</div>
                    <div>L2 Support</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="totalAgents">24</div>
                    <div>Total Agents</div>
                </div>
            </div>
        </div>

        <div class="controls">
            <div class="button-group">
                <button class="btn-primary" onclick="generateRoster()">Generate Roster</button>
                <button class="btn-success" onclick="saveRoster()">Save Roster</button>
                <button class="btn-danger" onclick="clearRoster()">Clear Roster</button>
                <button class="btn-primary" onclick="initializeTeam()">Initialize Team</button>
            </div>
            <div class="roster-controls">
                <input type="date" id="startDate" value="">
                <select id="weeksToShow" onchange="updateRosterDisplay()">
                    <option value="4" selected>4 Weeks</option>
                    <option value="8">8 Weeks</option>
                    <option value="12">12 Weeks</option>
                </select>
            </div>
        </div>

        <div style="display: flex; flex-wrap: wrap;">
            <div class="panel team-panel">
                <h3>Team Members</h3>
                <div class="team-list" id="teamList">
                    <!-- Team members will be listed here -->
                </div>
            </div>

            <div class="panel settings-panel">
                <h3>Shift Requirements</h3>
                <div>
                    <p><strong>Per Shift Requirements:</strong></p>
                    <ul>
                        <li>1 Team Lead (TL)</li>
                        <li>1-2 L3 Support</li>
                        <li>2-3 L2 Support</li>
                    </ul>
                    <p><strong>Shift Patterns:</strong></p>
                    <ul>
                        <li>5 consecutive morning shifts → 1-2 days off</li>
                        <li>5 consecutive afternoon shifts → 1-2 days off</li>
                        <li>5 consecutive night shifts → 2 days off</li>
                        <li>No morning shift after night shift</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="panel">
            <h3>Support Roster (4-Week View)</h3>
            <div id="rosterContainer">
                <!-- Roster table will be generated here -->
            </div>
        </div>

        <footer>
            <p>Naveen &copy; 2026 | Specialized for 24-member team structure</p>
        </footer>
    </div>

    <script>
        // Initialize data structures
        let teamMembers = JSON.parse(localStorage.getItem('supportTeam')) || [];
        let rosterData = JSON.parse(localStorage.getItem('rosterData')) || {};
        let currentStartDate = new Date();

        // Initialize with tomorrow's date
        const tomorrow = new Date(currentStartDate.getTime() + 24 * 60 * 60 * 1000);
        document.getElementById('startDate').valueAsDate = tomorrow;

        // Initialize team if empty
        if (teamMembers.length === 0) {
            initializeTeam();
        } else {
            renderTeamList();
        }
        updateRosterDisplay();

        function initializeTeam() {
            teamMembers = [];
            
            // Team Leads (7)
            const teamLeads = [
                { name: "Atul Dhamal", id: 1 },
                { name: "Durgeshkumar Singh", id: 2 },
                { name: "Mahesh Arokia", id: 3 },
                { name: "Mehul Dholakiya", id: 4 },
                { name: "Paras Shah", id: 5 },
                { name: "Rajkumar Chitravelu", id: 6 },
                { name: "Vigneshwaran Prakash", id: 7 }
            ];
            
            // L3 Support (5)
            const l3Support = [
                { name: "Arjun Ghadi", id: 8 },
                { name: "Ashish Chaturvedi", id: 9 },
                { name: "Ranjit Kumar S P", id: 10 },
                { name: "Sanjiv Sudhakar", id: 11 },
                { name: "Varad C N", id: 12 }
            ];
            
            // L2 Support (12)
            const l2Support = [
                { name: "Abhijeet Gorivale", id: 13 },
                { name: "Akash Sahu", id: 14 },
                { name: "Arsalan Shaikh", id: 15 },
                { name: "Athira Pillai", id: 16 },
                { name: "Fernando Gerard", id: 17 },
                { name: "Gandharv Adhikari", id: 18 },
                { name: "Mahadev Bhusnar", id: 19 },
                { name: "Mahesh Pawar", id: 20 },
                { name: "Manoj Khatri", id: 21 },
                { name: "Mehmood Nachan", id: 22 },
                { name: "Nitin Gadekar", id: 23 },
                { name: "Pranav Markande", id: 24 }
            ];
            
            // Add Team Leads
            teamLeads.forEach(tl => {
                teamMembers.push({
                    id: tl.id,
                    name: tl.name,
                    role: 'TL',
                    skills: ['TL', 'L3', 'L2'],
                    maxShifts: 35,
                    consecutiveShifts: { morning: 0, afternoon: 0, night: 0 },
                    lastShift: null,
                    daysOff: 0,
                    totalShifts: 0,
                    lastAssignment: null
                });
            });
            
            // Add L3 Support
            l3Support.forEach(l3 => {
                teamMembers.push({
                    id: l3.id,
                    name: l3.name,
                    role: 'L3',
                    skills: ['L3', 'L2'],
                    maxShifts: 35,
                    consecutiveShifts: { morning: 0, afternoon: 0, night: 0 },
                    lastShift: null,
                    daysOff: 0,
                    totalShifts: 0,
                    lastAssignment: null
                });
            });
            
            // Add L2 Support
            l2Support.forEach(l2 => {
                teamMembers.push({
                    id: l2.id,
                    name: l2.name,
                    role: 'L2',
                    skills: ['L2'],
                    maxShifts: 35,
                    consecutiveShifts: { morning: 0, afternoon: 0, night: 0 },
                    lastShift: null,
                    daysOff: 0,
                    totalShifts: 0,
                    lastAssignment: null
                });
            });
            
            saveTeamData();
            renderTeamList();
            showNotification('Team initialized with actual member names');
        }

        function renderTeamList() {
            const teamList = document.getElementById('teamList');
            teamList.innerHTML = '';
            
            // Sort by role
            const sortedTeam = [...teamMembers].sort((a, b) => {
                const roleOrder = { 'TL': 1, 'L3': 2, 'L2': 3 };
                return roleOrder[a.role] - roleOrder[b.role] || a.name.localeCompare(b.name);
            });
            
            sortedTeam.forEach(agent => {
                const div = document.createElement('div');
                div.className = 'team-member';
                div.innerHTML = `
                    <div>
                        <strong>${agent.name}</strong> (${agent.role})
                        <div class="agent-stats">
                            Total Shifts: ${agent.totalShifts} | 
                            Consecutive: M:${agent.consecutiveShifts.morning} A:${agent.consecutiveShifts.afternoon} N:${agent.consecutiveShifts.night} |
                            Days Off: ${agent.daysOff}
                        </div>
                    </div>
                `;
                teamList.appendChild(div);
            });
        }

        function isAgentAvailable(agent, shiftType, date) {
            // Check if agent is on leave
            if (agent.daysOff > 0) return false;
            
            // No morning shift after night shift
            if (shiftType === 'morning' && agent.lastShift === 'night') return false;
            
            // Check consecutive shift limits
            if (agent.consecutiveShifts[shiftType] >= 5) return false;
            
            return true;
        }

        function getAvailableAgentsByRole(role, shiftType, date) {
            return teamMembers.filter(agent => 
                agent.role === role && isAgentAvailable(agent, shiftType, date)
            );
        }

        function assignShift(agent, shiftType, date) {
            agent.consecutiveShifts[shiftType]++;
            agent.lastShift = shiftType;
            agent.totalShifts++;
            agent.lastAssignment = date;
            
            // Reset other consecutive counters
            Object.keys(agent.consecutiveShifts).forEach(type => {
                if (type !== shiftType) {
                    agent.consecutiveShifts[type] = 0;
                }
            });
            
            // Check if need to assign days off after 5 consecutive shifts
            if (agent.consecutiveShifts[shiftType] === 5) {
                agent.daysOff = shiftType === 'night' ? 2 : (Math.random() > 0.5 ? 2 : 1);
            }
        }

        function processDayOffs() {
            teamMembers.forEach(agent => {
                if (agent.daysOff > 0) {
                    agent.daysOff--;
                    if (agent.daysOff === 0) {
                        // Reset consecutive counters after break
                        agent.consecutiveShifts = { morning: 0, afternoon: 0, night: 0 };
                    }
                }
            });
        }

        function getLeastAssignedAgent(agents) {
            return agents.reduce((least, current) => 
                current.totalShifts < least.totalShifts ? current : least
            );
        }

        function generateRoster() {
            const startDate = new Date(document.getElementById('startDate').value);
            const weeks = parseInt(document.getElementById('weeksToShow').value);
            
            // Reset agent states
            teamMembers.forEach(agent => {
                agent.consecutiveShifts = { morning: 0, afternoon: 0, night: 0 };
                agent.lastShift = null;
                agent.daysOff = 0;
                agent.totalShifts = 0;
                agent.lastAssignment = null;
            });

            rosterData = {};
            const shifts = ['morning', 'afternoon', 'night'];

            for (let week = 0; week < weeks; week++) {
                for (let day = 0; day < 7; day++) {
                    const currentDate = new Date(startDate);
                    currentDate.setDate(startDate.getDate() + (week * 7) + day);
                    const dateString = currentDate.toISOString().split('T')[0];
                    
                    rosterData[dateString] = {};
                    
                    // Process day offs at start of each day
                    processDayOffs();
                    
                    shifts.forEach(shift => {
                        const assignedAgents = [];
                        
                        // Assign 1 TL (prefer least assigned)
                        const availableTLs = getAvailableAgentsByRole('TL', shift, currentDate);
                        if (availableTLs.length > 0) {
                            const tl = getLeastAssignedAgent(availableTLs);
                            assignedAgents.push(tl.name);
                            assignShift(tl, shift, currentDate);
                        }
                        
                        // Assign 1-2 L3 (prefer least assigned)
                        const availableL3s = getAvailableAgentsByRole('L3', shift, currentDate);
                        const l3Count = Math.min(1 + Math.floor(Math.random() * 2), availableL3s.length);
                        const selectedL3s = [];
                        for (let i = 0; i < l3Count && availableL3s.length > 0; i++) {
                            const l3 = getLeastAssignedAgent(availableL3s);
                            selectedL3s.push(l3);
                            availableL3s.splice(availableL3s.indexOf(l3), 1);
                        }
                        selectedL3s.forEach(l3 => {
                            assignedAgents.push(l3.name);
                            assignShift(l3, shift, currentDate);
                        });
                        
                        // Assign 2-3 L2 (prefer least assigned)
                        const availableL2s = getAvailableAgentsByRole('L2', shift, currentDate);
                        const l2Count = Math.min(2 + Math.floor(Math.random() * 2), availableL2s.length);
                        const selectedL2s = [];
                        for (let i = 0; i < l2Count && availableL2s.length > 0; i++) {
                            const l2 = getLeastAssignedAgent(availableL2s);
                            selectedL2s.push(l2);
                            availableL2s.splice(availableL2s.indexOf(l2), 1);
                        }
                        selectedL2s.forEach(l2 => {
                            assignedAgents.push(l2.name);
                            assignShift(l2, shift, currentDate);
                        });
                        
                        rosterData[dateString][shift] = assignedAgents;
                    });
                }
            }

            saveRosterData();
            renderTeamList();
            updateRosterDisplay();
            showNotification('Roster generated with actual team members!');
        }

        function updateRosterDisplay() {
            const container = document.getElementById('rosterContainer');
            const startDate = new Date(document.getElementById('startDate').value);
            const weeks = parseInt(document.getElementById('weeksToShow').value);

            const shifts = ['morning', 'afternoon', 'night'];
            const shiftNames = {
                'morning': 'Morning (07:00-16:00)',
                'afternoon': 'Afternoon (14:00-23:00)',
                'night': 'Night (22:30-07:30)'
            };

            let html = `<table class="roster-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Day</th>`;
            
            shifts.forEach(shift => {
                html += `<th>${shiftNames[shift]}</th>`;
            });
            
            html += `</tr></thead><tbody>`;

            for (let week = 0; week < weeks; week++) {
                for (let day = 0; day < 7; day++) {
                    const currentDate = new Date(startDate);
                    currentDate.setDate(startDate.getDate() + (week * 7) + day);
                    const dateString = currentDate.toISOString().split('T')[0];
                    const dayName = currentDate.toLocaleDateString('en-US', { weekday: 'long' });
                    
                    html += `<tr>
                        <td>${currentDate.toLocaleDateString()}</td>
                        <td>${dayName}</td>`;
                    
                    shifts.forEach(shift => {
                        const shiftClass = `shift-${shift}`;
                        const agents = rosterData[dateString] ? 
                            (rosterData[dateString][shift] || []) : [];
                        
                        html += `<td class="${shiftClass}">`;
                        agents.forEach(agent => {
                            const role = agent.includes(' ') ? 
                                teamMembers.find(m => m.name === agent)?.role : 
                                agent.split('-')[0];
                            const agentClass = `agent-${role?.toLowerCase() || 'l2'}`;
                            html += `<span class="${agentClass}">${agent}</span>`;
                        });
                        if (agents.length === 0) {
                            html += '<em>Not assigned</em>';
                        }
                        html += `</td>`;
                    });
                    
                    html += `</tr>`;
                }
                
                // Add week separator
                if (week < weeks - 1) {
                    html += `<tr><td colspan="${2 + shifts.length}" style="background: #f1c40f; color: white; text-align: center;">
                        <strong>Week ${week + 2} Starting</strong>
                    </td></tr>`;
                }
            }
            
            html += `</tbody></table>`;
            container.innerHTML = html;
        }

        function saveRoster() {
            saveRosterData();
            showNotification('Roster saved to browser storage!');
        }

        function clearRoster() {
            if (confirm('Are you sure you want to clear the current roster?')) {
                rosterData = {};
                saveRosterData();
                updateRosterDisplay();
                showNotification('Roster cleared');
            }
        }

        function saveTeamData() {
            localStorage.setItem('supportTeam', JSON.stringify(teamMembers));
        }

        function saveRosterData() {
            localStorage.setItem('rosterData', JSON.stringify(rosterData));
        }

        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.style.background = type === 'error' ? '#e74c3c' : '#27ae60';
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }

        // Auto-update when settings change
        document.getElementById('startDate').addEventListener('change', updateRosterDisplay);
    </script>
</body>
</html>
