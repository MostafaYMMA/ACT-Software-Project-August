/* =========================================================
   Project Data Models and Mock Data
   Prepared for easy backend integration
   ========================================================= */

// Mock data for all projects in the system
const ALL_PROJECTS = [
  // JL's projects
  { id: 'ledger-redesign', name: 'Ledger Redesign', code: 'ACT-001', desc: 'Refresh the dashboard UI and component library.', manager: 'John Lewis', managerInitials: 'JL', status: 'active', startDate: '2024-01-15', endDate: '2024-06-30', progress: 72, role: 'Project Manager', team: ['MB', 'AS'], availableSlots: 2, assignedTasks: 12 },
  { id: 'jl-performance-audit', name: 'Performance Audit', code: 'ACT-002', desc: 'Optimize app load times and reduce memory usage.', manager: 'John Lewis', managerInitials: 'JL', status: 'active', startDate: '2024-02-01', endDate: '2024-07-15', progress: 45, role: 'Project Manager', team: ['RK'], availableSlots: 3, assignedTasks: 8 },
  { id: 'jl-security-upgrade', name: 'Security Upgrade', code: 'ACT-003', desc: 'Implement OAuth 2.0 and improve authentication.', manager: 'John Lewis', managerInitials: 'JL', status: 'active', startDate: '2024-01-20', endDate: '2024-08-10', progress: 60, role: 'Project Manager', team: ['AS', 'DP'], availableSlots: 1, assignedTasks: 15 },
  { id: 'jl-analytics-dashboard', name: 'Analytics Dashboard', code: 'ACT-004', desc: 'Build real-time analytics and insights dashboard.', manager: 'John Lewis', managerInitials: 'JL', status: 'active', startDate: '2024-03-01', endDate: '2024-09-30', progress: 38, role: 'Project Manager', team: ['MB'], availableSlots: 4, assignedTasks: 10 },
  { id: 'jl-database-optimization', name: 'Database Optimization', code: 'ACT-005', desc: 'Refactor database schema and improve query performance.', manager: 'John Lewis', managerInitials: 'JL', status: 'active', startDate: '2024-02-10', endDate: '2024-08-30', progress: 55, role: 'Project Manager', team: ['RK', 'AS'], availableSlots: 2, assignedTasks: 14 },

  // MB's projects
  { id: 'onboarding', name: 'Onboarding Revamp', code: 'ACT-006', desc: 'Cut new-user time-to-first-task in half.', manager: 'Michelle Brown', managerInitials: 'MB', status: 'done', startDate: '2023-10-01', endDate: '2024-05-30', progress: 100, role: 'Team Member', team: [], availableSlots: 0, assignedTasks: 0 },
  { id: 'mb-user-testing', name: 'User Testing Program', code: 'ACT-007', desc: 'Recruit and conduct usability testing with 50 users.', manager: 'Michelle Brown', managerInitials: 'MB', status: 'active', startDate: '2024-03-15', endDate: '2024-10-30', progress: 35, role: 'Project Manager', team: ['TN'], availableSlots: 5, assignedTasks: 9 },
  { id: 'mb-help-center', name: 'Help Center Expansion', code: 'ACT-008', desc: 'Build comprehensive documentation and video guides.', manager: 'Michelle Brown', managerInitials: 'MB', status: 'active', startDate: '2024-02-20', endDate: '2024-09-15', progress: 78, role: 'Project Manager', team: ['JL'], availableSlots: 2, assignedTasks: 11 },
  { id: 'mb-customer-feedback', name: 'Customer Feedback Portal', code: 'ACT-009', desc: 'Create system for collecting and tracking user feedback.', manager: 'Michelle Brown', managerInitials: 'MB', status: 'active', startDate: '2024-03-01', endDate: '2024-11-30', progress: 42, role: 'Project Manager', team: ['AS', 'TN'], availableSlots: 3, assignedTasks: 8 },
  { id: 'mb-training-program', name: 'Training Program', code: 'ACT-010', desc: 'Develop comprehensive training materials for team.', manager: 'Michelle Brown', managerInitials: 'MB', status: 'active', startDate: '2024-04-01', endDate: '2024-10-31', progress: 65, role: 'Project Manager', team: ['JL', 'DP'], availableSlots: 2, assignedTasks: 7 },

  // AS's projects
  { id: 'reporting-api', name: 'Reporting API', code: 'ACT-011', desc: 'Expose task and team metrics via a public API.', manager: 'Andrea Smith', managerInitials: 'AS', status: 'active', startDate: '2024-01-10', endDate: '2024-07-31', progress: 88, role: 'Project Manager', team: ['DP', 'JL', 'MB'], availableSlots: 1, assignedTasks: 16 },
  { id: 'as-data-migration', name: 'Data Migration Tool', code: 'ACT-012', desc: 'Build importer for legacy task management systems.', manager: 'Andrea Smith', managerInitials: 'AS', status: 'active', startDate: '2024-02-15', endDate: '2024-08-20', progress: 52, role: 'Project Manager', team: ['RK'], availableSlots: 3, assignedTasks: 10 },
  { id: 'as-export-features', name: 'Export Features', code: 'ACT-013', desc: 'Add CSV, PDF, and Excel export capabilities.', manager: 'Andrea Smith', managerInitials: 'AS', status: 'active', startDate: '2024-03-10', endDate: '2024-09-20', progress: 68, role: 'Project Manager', team: ['MB'], availableSlots: 2, assignedTasks: 9 },
  { id: 'as-api-documentation', name: 'API Documentation', code: 'ACT-014', desc: 'Create complete API reference and integration guides.', manager: 'Andrea Smith', managerInitials: 'AS', status: 'active', startDate: '2024-04-01', endDate: '2024-10-15', progress: 48, role: 'Project Manager', team: ['TN', 'JL'], availableSlots: 4, assignedTasks: 6 },
  { id: 'as-webhook-system', name: 'Webhook System', code: 'ACT-015', desc: 'Implement webhook infrastructure for integrations.', manager: 'Andrea Smith', managerInitials: 'AS', status: 'active', startDate: '2024-02-25', endDate: '2024-09-10', progress: 61, role: 'Project Manager', team: ['RK', 'DP'], availableSlots: 2, assignedTasks: 12 },

  // RK's projects
  { id: 'mobile-app', name: 'Mobile App Beta', code: 'ACT-016', desc: 'Ship the first public beta to TestFlight.', manager: 'Robert Kim', managerInitials: 'RK', status: 'active', startDate: '2024-01-05', endDate: '2024-08-31', progress: 41, role: 'Project Manager', team: ['TN'], availableSlots: 3, assignedTasks: 13 },
  { id: 'rk-ios-release', name: 'iOS App Release', code: 'ACT-017', desc: 'Prepare iOS app for App Store submission.', manager: 'Robert Kim', managerInitials: 'RK', status: 'active', startDate: '2024-02-01', endDate: '2024-09-30', progress: 55, role: 'Project Manager', team: ['JL'], availableSlots: 2, assignedTasks: 11 },
  { id: 'rk-push-notifications', name: 'Push Notifications', code: 'ACT-018', desc: 'Implement real-time push notifications.', manager: 'Robert Kim', managerInitials: 'RK', status: 'active', startDate: '2024-03-05', endDate: '2024-10-10', progress: 42, role: 'Project Manager', team: ['AS', 'TN'], availableSlots: 3, assignedTasks: 8 },
  { id: 'rk-android-app', name: 'Android App Development', code: 'ACT-019', desc: 'Build native Android application.', manager: 'Robert Kim', managerInitials: 'RK', status: 'active', startDate: '2024-03-20', endDate: '2024-11-15', progress: 35, role: 'Project Manager', team: ['MB', 'TN'], availableSlots: 4, assignedTasks: 7 },
  { id: 'rk-offline-mode', name: 'Offline Mode', code: 'ACT-020', desc: 'Enable offline functionality and sync when online.', manager: 'Robert Kim', managerInitials: 'RK', status: 'active', startDate: '2024-04-10', endDate: '2024-12-20', progress: 28, role: 'Project Manager', team: ['AS'], availableSlots: 5, assignedTasks: 5 },

  // TN's projects
  { id: 'marketing-site', name: 'Q3 Marketing Site', code: 'ACT-021', desc: 'New landing page and pricing page copy.', manager: 'Tanya Ng', managerInitials: 'TN', status: 'paused', startDate: '2024-05-01', endDate: '2024-11-30', progress: 15, role: 'Project Manager', team: ['RK'], availableSlots: 2, assignedTasks: 4 },
  { id: 'tn-content-calendar', name: 'Content Calendar', code: 'ACT-022', desc: 'Plan and schedule social media content for Q3-Q4.', manager: 'Tanya Ng', managerInitials: 'TN', status: 'active', startDate: '2024-04-01', endDate: '2024-12-31', progress: 30, role: 'Project Manager', team: ['MB'], availableSlots: 3, assignedTasks: 6 },
  { id: 'tn-email-campaigns', name: 'Email Campaign Series', code: 'ACT-023', desc: 'Design onboarding and product announcement emails.', manager: 'Tanya Ng', managerInitials: 'TN', status: 'active', startDate: '2024-03-15', endDate: '2024-09-30', progress: 65, role: 'Project Manager', team: ['JL', 'RK'], availableSlots: 2, assignedTasks: 10 },
  { id: 'tn-branding-refresh', name: 'Branding Refresh', code: 'ACT-024', desc: 'Update logo, colors, and brand guidelines.', manager: 'Tanya Ng', managerInitials: 'TN', status: 'active', startDate: '2024-04-15', endDate: '2024-10-15', progress: 50, role: 'Project Manager', team: ['MB'], availableSlots: 2, assignedTasks: 8 },
  { id: 'tn-video-production', name: 'Video Production', code: 'ACT-025', desc: 'Produce product demo and tutorial videos.', manager: 'Tanya Ng', managerInitials: 'TN', status: 'active', startDate: '2024-05-01', endDate: '2024-12-15', progress: 22, role: 'Project Manager', team: ['RK', 'AS'], availableSlots: 4, assignedTasks: 5 },

  // DP's projects
  { id: 'team-directory', name: 'Team Directory', code: 'ACT-026', desc: 'Searchable directory with roles and availability.', manager: 'David Park', managerInitials: 'DP', status: 'active', startDate: '2024-02-20', endDate: '2024-08-31', progress: 55, role: 'Project Manager', team: ['AS'], availableSlots: 2, assignedTasks: 9 },
  { id: 'dp-org-chart', name: 'Organization Chart Tool', code: 'ACT-027', desc: 'Interactive org chart for larger teams.', manager: 'David Park', managerInitials: 'DP', status: 'active', startDate: '2024-03-10', endDate: '2024-10-20', progress: 38, role: 'Project Manager', team: ['MB', 'AS'], availableSlots: 3, assignedTasks: 7 },
  { id: 'dp-permissions-system', name: 'Permissions System', code: 'ACT-028', desc: 'Implement role-based access control (RBAC).', manager: 'David Park', managerInitials: 'DP', status: 'active', startDate: '2024-01-25', endDate: '2024-08-15', progress: 72, role: 'Project Manager', team: ['JL', 'RK'], availableSlots: 1, assignedTasks: 14 },
  { id: 'dp-audit-logging', name: 'Audit Logging System', code: 'ACT-029', desc: 'Track all user actions for compliance.', manager: 'David Park', managerInitials: 'DP', status: 'active', startDate: '2024-02-10', endDate: '2024-09-20', progress: 58, role: 'Project Manager', team: ['AS', 'JL'], availableSlots: 2, assignedTasks: 11 },
  { id: 'dp-backup-recovery', name: 'Backup & Recovery', code: 'ACT-030', desc: 'Implement automated backup and disaster recovery.', manager: 'David Park', managerInitials: 'DP', status: 'active', startDate: '2024-03-20', endDate: '2024-10-30', progress: 44, role: 'Project Manager', team: ['RK', 'TN'], availableSlots: 3, assignedTasks: 8 },
];

const PROJECT_STATUS_LABEL = { active: 'Active', paused: 'Paused', done: 'Completed' };
const PROJECT_STATUS_CLASS = { active: 'status-active', paused: 'status-paused', done: 'status-done' };

/**
 * Get all available projects (not managed by the current user)
 */
function getAvailableProjects(currentUserInitials) {
  return ALL_PROJECTS.filter(p => p.managerInitials !== currentUserInitials);
}

/**
 * Get user's own projects
 */
function getMyProjects(currentUserInitials) {
  return ALL_PROJECTS.filter(p => p.managerInitials === currentUserInitials);
}

/**
 * Render available projects grid
 */
function renderAvailableProjects(container, searchTerm = '') {
  if(!container) return;
  
  const currentUserInitials = resolveProjectManager(Store.currentUser());
  let projects = getAvailableProjects(currentUserInitials);
  
  // Filter by search term
  if(searchTerm.trim()){
    const term = searchTerm.toLowerCase();
    projects = projects.filter(p => 
      p.name.toLowerCase().includes(term) || 
      p.code.toLowerCase().includes(term) || 
      p.desc.toLowerCase().includes(term)
    );
  }
  
  if(projects.length === 0){
    container.innerHTML = `
      <div class="empty-state" style="grid-column: 1/-1; padding: 40px 20px; text-align: center;">
        <div class="glyph">📁</div>
        <div>No available projects</div>
      </div>`;
    return;
  }
  
  container.innerHTML = projects.map(p => `
    <div class="project-card">
      <div class="project-header">
        <div class="project-code">${p.code}</div>
        <span class="status-badge ${PROJECT_STATUS_CLASS[p.status]}">${PROJECT_STATUS_LABEL[p.status]}</span>
      </div>
      <div class="project-title">${p.name}</div>
      <div class="project-desc">${p.desc}</div>
      <div class="project-meta">
        <div class="meta-row">
          <span class="meta-label">Manager:</span>
          <span class="meta-value">${p.manager}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Start:</span>
          <span class="meta-value">${formatDate(p.startDate)}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Available Slots:</span>
          <span class="meta-value">${p.availableSlots}</span>
        </div>
      </div>
      <div class="project-action">
        <button class="btn-primary" onclick="window.location.href='project-detail.html?id=${encodeURIComponent(p.id)}'">View Project</button>
      </div>
    </div>
  `).join('');
}

/**
 * Render my projects grid
 */
function renderMyProjects(container, user, searchTerm = '') {
  if(!container) return;
  
  const currentUserInitials = resolveProjectManager(user);
  let projects = getMyProjects(currentUserInitials);
  
  // Filter by search term
  if(searchTerm.trim()){
    const term = searchTerm.toLowerCase();
    projects = projects.filter(p => 
      p.name.toLowerCase().includes(term) || 
      p.code.toLowerCase().includes(term) || 
      p.desc.toLowerCase().includes(term)
    );
  }
  
  if(projects.length === 0){
    container.innerHTML = `
      <div class="empty-state" style="grid-column: 1/-1; padding: 40px 20px; text-align: center;">
        <div class="glyph">📁</div>
        <div>You have no projects assigned yet</div>
      </div>`;
    return;
  }
  
  container.innerHTML = projects.map(p => `
    <div class="project-card my-project-card">
      <div class="project-header">
        <div class="project-code">${p.code}</div>
        <span class="status-badge ${PROJECT_STATUS_CLASS[p.status]}">${PROJECT_STATUS_LABEL[p.status]}</span>
      </div>
      <div class="project-title">${p.name}</div>
      <div class="project-desc">${p.desc}</div>
      
      <div class="project-progress">
        <div class="progress-label"><span>Progress</span><span>${p.progress}%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:${p.progress}%"></div></div>
      </div>
      
      <div class="project-meta">
        <div class="meta-row">
          <span class="meta-label">Role:</span>
          <span class="meta-value">${p.role}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Tasks:</span>
          <span class="meta-value">${p.assignedTasks}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Team Size:</span>
          <span class="meta-value">${p.team.length} members</span>
        </div>
      </div>
      
      <div class="project-action">
        <button class="btn-primary" onclick="window.location.href='project-detail.html?id=${encodeURIComponent(p.id)}'">View Project</button>
      </div>
    </div>
  `).join('');
}

/**
 * Format date for display
 */
function formatDate(dateStr) {
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  } catch(e) {
    return dateStr;
  }
}

/**
 * Initialize projects dropdown behavior
 */
function initProjectsDropdown(){
  const toggle = document.querySelector('[data-projects-toggle]');
  const submenu = document.querySelector('[data-projects-submenu]');
  
  if(!toggle || !submenu) return;
  if(toggle.dataset.bound === 'true') return;
  toggle.dataset.bound = 'true';
  
  // Default: expand submenu on the project pages.
  submenu.classList.add('open');
  toggle.classList.add('expanded');
  
  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    const isOpen = submenu.classList.toggle('open');
    toggle.classList.toggle('expanded', isOpen);
  });
  
  // Update active submenu link based on current page
  const currentPage = window.location.pathname.split('/').pop();
  const submenuLinks = document.querySelectorAll('[data-submenu-page]');
  submenuLinks.forEach(link => {
    link.classList.remove('active');
  });
  
  if(currentPage === 'available-projects.html'){
    document.querySelector('[data-submenu-page="available"]')?.classList.add('active');
  } else if(currentPage === 'my-projects.html'){
    document.querySelector('[data-submenu-page="my"]')?.classList.add('active');
  }
}

if (typeof globalThis !== 'undefined') {
  globalThis.ALL_PROJECTS = ALL_PROJECTS;
  globalThis.getAvailableProjects = getAvailableProjects;
  globalThis.getMyProjects = getMyProjects;
  globalThis.renderAvailableProjects = renderAvailableProjects;
  globalThis.renderMyProjects = renderMyProjects;
  globalThis.formatDate = formatDate;
  globalThis.initProjectsDropdown = initProjectsDropdown;
}
