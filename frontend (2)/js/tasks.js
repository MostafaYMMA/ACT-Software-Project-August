/* =========================================================
   ACT — task CRUD + rendering helpers
   ========================================================= */

const PRIORITY_LABEL = { high: 'High', med: 'Medium', low: 'Low' };
const PRIORITY_CHIP  = { high: 'chip-high', med: 'chip-med', low: 'chip-low' };
const PRIORITY_ORDER = { high: 0, med: 1, low: 2 };

// Project list (reference for task assignments)
const PROJECT_LIST = [
  // John Lewis
  { id: 'ledger-redesign', name: 'Ledger Redesign' },
  { id: 'jl-performance-audit', name: 'Performance Audit' },
  { id: 'jl-security-upgrade', name: 'Security Upgrade' },
  { id: 'jl-analytics-dashboard', name: 'Analytics Dashboard' },
  { id: 'jl-database-optimization', name: 'Database Optimization' },
  // Michelle Brown
  { id: 'onboarding', name: 'Onboarding Revamp' },
  { id: 'mb-user-testing', name: 'User Testing Program' },
  { id: 'mb-help-center', name: 'Help Center Expansion' },
  { id: 'mb-customer-feedback', name: 'Customer Feedback Portal' },
  { id: 'mb-training-program', name: 'Training Program' },
  // Andrea Smith
  { id: 'reporting-api', name: 'Reporting API' },
  { id: 'as-data-migration', name: 'Data Migration Tool' },
  { id: 'as-export-features', name: 'Export Features' },
  { id: 'as-api-documentation', name: 'API Documentation' },
  { id: 'as-webhook-system', name: 'Webhook System' },
  // Robert Kim
  { id: 'mobile-app', name: 'Mobile App Beta' },
  { id: 'rk-ios-release', name: 'iOS App Release' },
  { id: 'rk-push-notifications', name: 'Push Notifications' },
  { id: 'rk-android-app', name: 'Android App Development' },
  { id: 'rk-offline-mode', name: 'Offline Mode' },
  // Tanya Ng
  { id: 'marketing-site', name: 'Q3 Marketing Site' },
  { id: 'tn-content-calendar', name: 'Content Calendar' },
  { id: 'tn-email-campaigns', name: 'Email Campaign Series' },
  { id: 'tn-branding-refresh', name: 'Branding Refresh' },
  { id: 'tn-video-production', name: 'Video Production' },
  // David Park
  { id: 'team-directory', name: 'Team Directory' },
  { id: 'dp-org-chart', name: 'Organization Chart Tool' },
  { id: 'dp-permissions-system', name: 'Permissions System' },
  { id: 'dp-audit-logging', name: 'Audit Logging System' },
  { id: 'dp-backup-recovery', name: 'Backup & Recovery' },
  // Mariam Hassan
  { id: 'mh-mobile-ui', name: 'Mobile UI Kit' },
  { id: 'mh-design-system', name: 'Design System v2' },
  // Sofia Rodriguez
  { id: 'sr-customer-success', name: 'Customer Success Hub' },
  { id: 'sr-knowledge-base', name: 'Knowledge Base Rebuild' },
  { id: 'sr-community-forum', name: 'Community Forum' },
  { id: 'sr-feedback-system', name: 'Feedback Management' },
  { id: 'sr-onboarding-flows', name: 'Onboarding Flows' },
  // Elena Kowalski
  { id: 'ek-performance-metrics', name: 'Performance Metrics' },
  { id: 'ek-testing-framework', name: 'Testing Framework' },
  { id: 'ek-ci-cd-pipeline', name: 'CI/CD Pipeline' },
  { id: 'ek-infrastructure', name: 'Infrastructure as Code' },
  { id: 'ek-monitoring-alerts', name: 'Monitoring & Alerts' },
];

function getProjectName(projectId) {
  const project = PROJECT_LIST.find(p => p.id === projectId);
  return project ? project.name : projectId;
}

function relativeDay(ts){
  const days = Math.floor((Date.now() - ts) / 86400000);
  if(days <= 0) return 'today';
  if(days === 1) return 'yesterday';
  return `${days}d ago`;
}

function taskRowHTML(task){
  return `
    <div class="task-row ${task.done ? 'done' : ''}" data-id="${task.id}">
      <input type="checkbox" class="stamp" ${task.done ? 'checked' : ''} aria-label="Mark task done" />
      <div class="task-main">
        <div class="task-title">${escapeHTML(task.title)}</div>
        <div class="task-meta">
          <span class="chip ${PRIORITY_CHIP[task.priority]}">${PRIORITY_LABEL[task.priority]}</span>
          <span class="chip chip-project">${getProjectName(task.project)}</span>
          <span>added ${relativeDay(task.createdAt)}</span>
        </div>
      </div>
      <button class="task-delete" aria-label="Delete task" title="Delete task">&times;</button>
    </div>`;
  }

function escapeHTML(str){
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

/**
 * Renders a task list into `container` for the given email, applying
 * `filterFn` (task => bool) and wiring toggle/delete + calling `onChange`
 * after every mutation so the caller can refresh counts/stats.
 */
function renderTaskList(container, email, filterFn, onChange, emptyMessage){
  const all = Store.getTasks(email);
  const visible = all.filter(filterFn).sort((a, b) => a.done - b.done || PRIORITY_ORDER[a.priority] - PRIORITY_ORDER[b.priority]);

  if(!visible.length){
    container.innerHTML = `
      <div class="empty-state">
        <div class="glyph">&#9744;</div>
        <div>${emptyMessage || 'No tasks here yet.'}</div>
      </div>`;
    return;
  }

  container.innerHTML = visible.map(taskRowHTML).join('');

  container.querySelectorAll('.task-row').forEach(row => {
    const id = row.dataset.id;

    row.querySelector('.stamp').addEventListener('change', (e) => {
      const tasks = Store.getTasks(email);
      const t = tasks.find(t => t.id === id);
      if(t){ t.done = e.target.checked; Store.saveTasks(email, tasks); }
      row.classList.toggle('done', e.target.checked);
      onChange && onChange();
    });

    row.querySelector('.task-delete').addEventListener('click', () => {
      const tasks = Store.getTasks(email).filter(t => t.id !== id);
      Store.saveTasks(email, tasks);
      row.remove();
      onChange && onChange();
      if(!container.querySelector('.task-row')){
        renderTaskList(container, email, filterFn, onChange, emptyMessage);
      }
    });
  });
}

function addTask(email, {title, priority, project}){
  if(!project) throw new Error('Project is required for a task');
  const tasks = Store.getTasks(email);
  tasks.unshift({
    id: crypto.randomUUID(),
    title,
    priority,
    project: project,
    done: false,
    createdAt: Date.now()
  });
  Store.saveTasks(email, tasks);
}

function taskStats(email, managedProjectIds){
  let tasks = Store.getTasks(email);
  
  // If managedProjectIds provided, filter by those projects
  if(managedProjectIds && Array.isArray(managedProjectIds)){
    tasks = tasks.filter(t => managedProjectIds.includes(t.project));
  }
  
  const done = tasks.filter(t => t.done).length;
  const open = tasks.length - done;
  const byPriority = { high: 0, med: 0, low: 0 };
  tasks.forEach(t => { if(!t.done) byPriority[t.priority]++; });
  const completion = tasks.length ? Math.round((done / tasks.length) * 100) : 0;
  return { total: tasks.length, done, open, byPriority, completion };
}
