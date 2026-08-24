/* =========================================================
   ACT — Projects page (mock data, no backend yet)
   ========================================================= */

const PROJECTS = [
  // John Lewis (JL) - 5 projects
  { id: 'ledger-redesign', name: 'Ledger Redesign',        desc: 'Refresh the dashboard UI and component library.',        progress: 72, status: 'active', projectManager: 'JL', team: ['MB', 'AS'] },
  { id: 'jl-performance-audit', name: 'Performance Audit',      desc: 'Optimize app load times and reduce memory usage.',                 progress: 45, status: 'active', projectManager: 'JL', team: ['RK'] },
  { id: 'jl-security-upgrade', name: 'Security Upgrade',    desc: 'Implement OAuth 2.0 and improve authentication.',           progress: 60, status: 'active', projectManager: 'JL', team: ['AS', 'DP'] },
  { id: 'jl-analytics-dashboard', name: 'Analytics Dashboard', desc: 'Build real-time analytics and insights dashboard.',     progress: 38, status: 'active', projectManager: 'JL', team: ['MB'] },
  { id: 'jl-database-optimization', name: 'Database Optimization', desc: 'Refactor database schema and improve query performance.', progress: 55, status: 'active', projectManager: 'JL', team: ['RK', 'AS'] },

  // Michelle Brown (MB) - 5 projects
  { id: 'onboarding', name: 'Onboarding Revamp',      desc: 'Cut new-user time-to-first-task in half.',                 progress: 100, status: 'done', projectManager: 'MB', team: [] },
  { id: 'mb-user-testing', name: 'User Testing Program',    desc: 'Recruit and conduct usability testing with 50 users.',      progress: 35, status: 'active', projectManager: 'MB', team: ['TN'] },
  { id: 'mb-help-center', name: 'Help Center Expansion',    desc: 'Build comprehensive documentation and video guides.',       progress: 78, status: 'active', projectManager: 'MB', team: ['JL'] },
  { id: 'mb-customer-feedback', name: 'Customer Feedback Portal', desc: 'Create system for collecting and tracking user feedback.',  progress: 42, status: 'active', projectManager: 'MB', team: ['AS', 'TN'] },
  { id: 'mb-training-program', name: 'Training Program',     desc: 'Develop comprehensive training materials for team.',      progress: 65, status: 'active', projectManager: 'MB', team: ['JL', 'DP'] },

  // Andrea Smith (AS) - 5 projects
  { id: 'reporting-api', name: 'Reporting API',          desc: 'Expose task and team metrics via a public API.',           progress: 88, status: 'active', projectManager: 'AS', team: ['DP', 'JL', 'MB'] },
  { id: 'as-data-migration', name: 'Data Migration Tool',    desc: 'Build importer for legacy task management systems.',      progress: 52, status: 'active', projectManager: 'AS', team: ['RK'] },
  { id: 'as-export-features', name: 'Export Features',       desc: 'Add CSV, PDF, and Excel export capabilities.',            progress: 68, status: 'active', projectManager: 'AS', team: ['MB'] },
  { id: 'as-api-documentation', name: 'API Documentation', desc: 'Create complete API reference and integration guides.',   progress: 48, status: 'active', projectManager: 'AS', team: ['TN', 'JL'] },
  { id: 'as-webhook-system', name: 'Webhook System',       desc: 'Implement webhook infrastructure for integrations.',       progress: 61, status: 'active', projectManager: 'AS', team: ['RK', 'DP'] },

  // Robert Kim (RK) - 5 projects
  { id: 'mobile-app', name: 'Mobile App Beta',        desc: 'Ship the first public beta to TestFlight.',                progress: 41, status: 'active', projectManager: 'RK', team: ['TN'] },
  { id: 'rk-ios-release', name: 'iOS App Release',       desc: 'Prepare iOS app for App Store submission.',                progress: 55, status: 'active', projectManager: 'RK', team: ['JL'] },
  { id: 'rk-push-notifications', name: 'Push Notifications', desc: 'Implement real-time push notifications.',                  progress: 42, status: 'active', projectManager: 'RK', team: ['AS', 'TN'] },
  { id: 'rk-android-app', name: 'Android App Development', desc: 'Build native Android application.',                    progress: 35, status: 'active', projectManager: 'RK', team: ['MB', 'TN'] },
  { id: 'rk-offline-mode', name: 'Offline Mode',          desc: 'Enable offline functionality and sync when online.',       progress: 28, status: 'active', projectManager: 'RK', team: ['AS'] },

  // Tanya Ng (TN) - 5 projects
  { id: 'marketing-site', name: 'Q3 Marketing Site',      desc: 'New landing page and pricing page copy.',                  progress: 15, status: 'paused', projectManager: 'TN', team: ['RK'] },
  { id: 'tn-content-calendar', name: 'Content Calendar',     desc: 'Plan and schedule social media content for Q3-Q4.',     progress: 30, status: 'active', projectManager: 'TN', team: ['MB'] },
  { id: 'tn-email-campaigns', name: 'Email Campaign Series', desc: 'Design onboarding and product announcement emails.',      progress: 65, status: 'active', projectManager: 'TN', team: ['JL', 'RK'] },
  { id: 'tn-branding-refresh', name: 'Branding Refresh',     desc: 'Update logo, colors, and brand guidelines.',              progress: 50, status: 'active', projectManager: 'TN', team: ['MB'] },
  { id: 'tn-video-production', name: 'Video Production',    desc: 'Produce product demo and tutorial videos.',               progress: 22, status: 'active', projectManager: 'TN', team: ['RK', 'AS'] },

  // David Park (DP) - 5 projects
  { id: 'team-directory', name: 'Team Directory',         desc: 'Searchable directory with roles and availability.',        progress: 55, status: 'active', projectManager: 'DP', team: ['AS'] },
  { id: 'dp-org-chart', name: 'Organization Chart Tool',    desc: 'Interactive org chart for larger teams.',                 progress: 38, status: 'active', projectManager: 'DP', team: ['MB', 'AS'] },
  { id: 'dp-permissions-system', name: 'Permissions System', desc: 'Implement role-based access control (RBAC).',             progress: 72, status: 'active', projectManager: 'DP', team: ['JL', 'RK'] },
  { id: 'dp-audit-logging', name: 'Audit Logging System',  desc: 'Track all user actions for compliance.',                    progress: 58, status: 'active', projectManager: 'DP', team: ['AS', 'JL'] },
  { id: 'dp-backup-recovery', name: 'Backup & Recovery',   desc: 'Implement automated backup and disaster recovery.',        progress: 44, status: 'active', projectManager: 'DP', team: ['RK', 'TN'] },

  // Mariam Hassan (MH) - 2 projects
  { id: 'mh-mobile-ui', name: 'Mobile UI Kit',             desc: 'Design comprehensive mobile UI component library.',        progress: 76, status: 'active', projectManager: 'MH', team: ['RK', 'TN'] },
  { id: 'mh-design-system', name: 'Design System v2',       desc: 'Overhaul design system with new tokens and components.',    progress: 63, status: 'active', projectManager: 'MH', team: ['JL', 'MB'] },

  // Sofia Rodriguez (SR) - 5 projects
  { id: 'sr-customer-success', name: 'Customer Success Hub', desc: 'Build dedicated support and success management platform.',   progress: 58, status: 'active', projectManager: 'SR', team: ['MB', 'TN'] },
  { id: 'sr-knowledge-base', name: 'Knowledge Base Rebuild', desc: 'Modernize knowledge base with AI search and categorization.', progress: 47, status: 'active', projectManager: 'SR', team: ['JL'] },
  { id: 'sr-community-forum', name: 'Community Forum',       desc: 'Launch user community forum for peer support.',             progress: 34, status: 'active', projectManager: 'SR', team: ['MB', 'AS'] },
  { id: 'sr-feedback-system', name: 'Feedback Management',   desc: 'Implement structured user feedback collection system.',     progress: 69, status: 'active', projectManager: 'SR', team: ['DP'] },
  { id: 'sr-onboarding-flows', name: 'Onboarding Flows',     desc: 'Design personalized onboarding paths by user type.',        progress: 55, status: 'active', projectManager: 'SR', team: ['JL', 'MB', 'TN'] },

  // Elena Kowalski (EK) - 5 projects
  { id: 'ek-performance-metrics', name: 'Performance Metrics', desc: 'Build real-time performance monitoring dashboard.',        progress: 64, status: 'active', projectManager: 'EK', team: ['AS', 'JL'] },
  { id: 'ek-testing-framework', name: 'Testing Framework',   desc: 'Establish E2E testing framework and best practices.',      progress: 71, status: 'active', projectManager: 'EK', team: ['RK', 'DP'] },
  { id: 'ek-ci-cd-pipeline', name: 'CI/CD Pipeline',         desc: 'Optimize and automate deployment pipeline.',               progress: 85, status: 'active', projectManager: 'EK', team: ['JL', 'AS'] },
  { id: 'ek-infrastructure', name: 'Infrastructure as Code',  desc: 'Migrate infrastructure to IaC with Terraform.',            progress: 52, status: 'active', projectManager: 'EK', team: ['RK', 'DP'] },
  { id: 'ek-monitoring-alerts', name: 'Monitoring & Alerts',  desc: 'Implement comprehensive monitoring and alerting system.',    progress: 73, status: 'active', projectManager: 'EK', team: ['AS'] },
];

const STATUS_LABEL = { active: 'Active', paused: 'Paused', done: 'Done' };
const STATUS_CHIP  = { active: 'chip-active', paused: 'chip-paused', done: 'chip-done' };

function renderProjects(container, userInitials){
  const userProjects = PROJECTS.filter(p => p.projectManager === userInitials);
  
  if(!userProjects.length){
    container.innerHTML = `
      <div class="empty-state" style="grid-column: 1/-1; padding: 40px 20px; text-align: center;">
        <div class="glyph">📁</div>
        <div>No available projects</div>
      </div>`;
    return;
  }
  
  container.innerHTML = userProjects.map(p => `
    <a class="project-card-link" href="project-detail.html?id=${encodeURIComponent(p.id)}" aria-label="Open project ${p.name}">
      <div class="project-card ${p.status === 'done' ? 'done' : ''}">
        <div class="project-top">
          <div class="project-name">${p.name}</div>
          <span class="chip ${STATUS_CHIP[p.status]}">${STATUS_LABEL[p.status]}</span>
        </div>
        <div class="project-desc">${p.desc}</div>
        <div class="project-manager-badge">
          <span class="manager-label">Project Manager:</span>
          <div class="mini-avatar mini-avatar-manager">${p.projectManager}</div>
        </div>
        <div class="project-progress">
          <div class="progress-label"><span>Progress</span><span>${p.progress}%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:${p.progress}%"></div></div>
        </div>
        <div class="project-foot">
          <div class="avatar-stack">
            ${p.team.length > 0 ? p.team.map(i => `<div class="mini-avatar">${i}</div>`).join('') : '<span class="no-team">No team members</span>'}
          </div>
        </div>
      </div>
    </a>
  `).join('');
}
