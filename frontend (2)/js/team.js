/* =========================================================
   ACT — Team page (mock data, no backend yet)
   ========================================================= */

const TEAM = [
  { name: 'Jordan Lee',    role: 'Product Manager',   status: 'active' },
  { name: 'Maya Brooks',   role: 'Frontend Engineer', status: 'active' },
  { name: 'Amir Siddiqui', role: 'Backend Engineer',  status: 'active' },
  { name: 'Dana Park',     role: 'UX Designer',       status: 'active' },
  { name: 'Ravi Kapoor',   role: 'QA Engineer',       status: 'paused' },
  { name: 'Talia Novak',   role: 'Marketing Lead',    status: 'active' },
];

function renderTeam(container){
  container.innerHTML = TEAM.map(m => `
    <a href="employee-detail.html?name=${encodeURIComponent(m.name)}" class="team-card team-card-link">
      <div class="avatar-lg">${initials(m.name)}</div>
      <div class="who">
        <div class="t-name">${m.name}</div>
        <div class="t-role">${m.role}</div>
        <div class="t-status"><span class="chip ${m.status === 'active' ? 'chip-active' : 'chip-paused'}">${m.status === 'active' ? 'Active' : 'Away'}</span></div>
      </div>
    </a>
  `).join('');
}
