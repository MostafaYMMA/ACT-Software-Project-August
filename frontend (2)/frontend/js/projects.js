/* =========================================================
   ACT — Projects page (mock data, no backend yet)
   ========================================================= */

const PROJECTS = [
  { name: 'Ledger Redesign',        desc: 'Refresh the dashboard UI and component library.',        progress: 72, status: 'active', team: ['JL', 'MB', 'AS'] },
  { name: 'Mobile App Beta',        desc: 'Ship the first public beta to TestFlight.',                progress: 41, status: 'active', team: ['RK', 'TN'] },
  { name: 'Reporting API',          desc: 'Expose task and team metrics via a public API.',           progress: 88, status: 'active', team: ['AS', 'DP', 'JL', 'MB'] },
  { name: 'Onboarding Revamp',      desc: 'Cut new-user time-to-first-task in half.',                 progress: 100, status: 'done', team: ['MB'] },
  { name: 'Q3 Marketing Site',      desc: 'New landing page and pricing page copy.',                  progress: 15, status: 'paused', team: ['TN', 'RK'] },
  { name: 'Team Directory',         desc: 'Searchable directory with roles and availability.',        progress: 55, status: 'active', team: ['DP', 'AS'] },
];

const STATUS_LABEL = { active: 'Active', paused: 'Paused', done: 'Done' };
const STATUS_CHIP  = { active: 'chip-active', paused: 'chip-paused', done: 'chip-done' };

function renderProjects(container){
  container.innerHTML = PROJECTS.map(p => `
    <div class="project-card">
      <div class="project-top">
        <div class="project-name">${p.name}</div>
        <span class="chip ${STATUS_CHIP[p.status]}">${STATUS_LABEL[p.status]}</span>
      </div>
      <div class="project-desc">${p.desc}</div>
      <div class="project-progress">
        <div class="progress-label"><span>Progress</span><span>${p.progress}%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:${p.progress}%"></div></div>
      </div>
      <div class="project-foot">
        <div class="avatar-stack">
          ${p.team.map(i => `<div class="mini-avatar">${i}</div>`).join('')}
        </div>
      </div>
    </div>
  `).join('');
}
