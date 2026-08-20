/* =========================================================
   ACT — shared app utilities
   Demo-only auth: users + sessions live in localStorage.
   Swap Store.* for real API calls when a backend exists.
   ========================================================= */

const Store = {
  USERS_KEY: 'act_users',
  SESSION_KEY: 'act_session',
  SIDEBAR_KEY: 'act_sidebar_collapsed',
  THEME_KEY: 'act_theme',

  getUsers(){
    try{ return JSON.parse(localStorage.getItem(this.USERS_KEY)) || []; }
    catch(e){ return []; }
  },
  saveUsers(users){ localStorage.setItem(this.USERS_KEY, JSON.stringify(users)); },

  findUser(email){
    return this.getUsers().find(u => u.email.toLowerCase() === email.toLowerCase());
  },

  createUser({name, email, password}){
    const users = this.getUsers();
    users.push({name, email, password, createdAt: Date.now()});
    this.saveUsers(users);
  },

  setSession(email){ localStorage.setItem(this.SESSION_KEY, email); },
  getSession(){ return localStorage.getItem(this.SESSION_KEY); },
  clearSession(){ localStorage.removeItem(this.SESSION_KEY); },

  currentUser(){
    const email = this.getSession();
    if(!email) return null;
    return this.findUser(email) || null;
  },

  tasksKey(email){ return `act_tasks_${email.toLowerCase()}`; },

  getTasks(email){
    try{ return JSON.parse(localStorage.getItem(this.tasksKey(email))) || []; }
    catch(e){ return []; }
  },
  saveTasks(email, tasks){
    localStorage.setItem(this.tasksKey(email), JSON.stringify(tasks));
  },

  seedTasksIfEmpty(email){
    if(this.getTasks(email).length) return;
    const now = Date.now();
    this.saveTasks(email, [
      { id: crypto.randomUUID(), title: 'Wireframe the onboarding flow', priority: 'high', project: 'onboarding', done: false, createdAt: now - 86400000 * 2 },
      { id: crypto.randomUUID(), title: 'Review pull request #114',      priority: 'med',  project: 'ledger-redesign', done: false, createdAt: now - 86400000 },
      { id: crypto.randomUUID(), title: 'Write weekly status update',    priority: 'low',  project: 'reporting-api', done: true,  createdAt: now - 86400000 * 3 },
      { id: crypto.randomUUID(), title: 'Sync with design on sidebar UI', priority: 'med', project: 'ledger-redesign', done: true,  createdAt: now - 86400000 * 4 },
    ]);
  },

  cleanOldTasks(email){
    const tasks = this.getTasks(email);
    const validTasks = tasks.filter(t => t.project);
    if(validTasks.length < tasks.length){
      this.saveTasks(email, validTasks);
    }
  },

  seedUsersIfEmpty(){
    if(this.getUsers().length) return;
    this.createUser({ name: 'John Lewis', email: 'jl@example.com', password: 'password' });
    this.createUser({ name: 'Michelle Brown', email: 'mb@example.com', password: 'password' });
    this.createUser({ name: 'Andrea Smith', email: 'as@example.com', password: 'password' });
    this.createUser({ name: 'Robert Kim', email: 'rk@example.com', password: 'password' });
    this.createUser({ name: 'Tanya Ng', email: 'tn@example.com', password: 'password' });
    this.createUser({ name: 'David Park', email: 'dp@example.com', password: 'password' });
    this.createUser({ name: 'Mariam Hassan', email: 'mariam@example.com', password: 'password' });
    this.createUser({ name: 'Sofia Rodriguez', email: 'sofia@example.com', password: 'password' });
    this.createUser({ name: 'Elena Kowalski', email: 'elena@example.com', password: 'password' });
  }
};

// Seed demo users on app load
Store.seedUsersIfEmpty();

/* =========================================================
   DARK MODE
   ========================================================= */

function initTheme(){
  const savedTheme = localStorage.getItem(Store.THEME_KEY);

  if(savedTheme === 'dark'){
    document.body.classList.add('dark-mode');
  }
}

function createThemeToggle(){

  const headerRight = document.querySelector('.header-right');

  if(!headerRight) return;

  if(headerRight.querySelector('.theme-toggle')) return;

  const button = document.createElement('button');

  button.type = 'button';
  button.className = 'theme-toggle';

  button.setAttribute(
    'aria-label',
    'Toggle dark mode'
  );

  updateThemeButton(button);

  button.addEventListener('click', () => {

    document.body.classList.toggle('dark-mode');

    const isDark =
      document.body.classList.contains('dark-mode');

    localStorage.setItem(
      Store.THEME_KEY,
      isDark ? 'dark' : 'light'
    );

    updateThemeButton(button);
  });

  headerRight.insertBefore(
    button,
    headerRight.firstElementChild
  );
}

function updateThemeButton(button){

  const isDark =
    document.body.classList.contains('dark-mode');

  button.textContent = isDark ? '☀️' : '🌙';
}

/** Redirect to login if no session; call at top of protected pages. */
function requireAuth(){
  const user = Store.currentUser();
  if(!user){
    window.location.href = 'index.html';
    return null;
  }
  Store.seedTasksIfEmpty(user.email);
  Store.cleanOldTasks(user.email);
  return user;
}

function initials(name){
  return (name || '').trim().split(/\s+/).slice(0,2).map(p => p[0].toUpperCase()).join('');
}

const PROJECT_MANAGER_MAP = {
  'jl@example.com': 'JL',
  'john lewis': 'JL',
  'mb@example.com': 'MB',
  'michelle brown': 'MB',
  'as@example.com': 'AS',
  'andrea smith': 'AS',
  'rk@example.com': 'RK',
  'robert kim': 'RK',
  'tn@example.com': 'TN',
  'tanya ng': 'TN',
  'dp@example.com': 'DP',
  'david park': 'DP',
  'mariam@example.com': 'MH',
  'mariam': 'MH',
  'mariam hassan': 'MH',
  'sofia@example.com': 'SR',
  'sofia': 'SR',
  'sofia rodriguez': 'SR',
  'elena@example.com': 'EK',
  'elena': 'EK',
  'elena kowalski': 'EK'
};

function resolveProjectManager(user){
  if(!user) return '';

  const emailKey = String(user.email || '').trim().toLowerCase();
  const nameKey = String(user.name || '').trim().toLowerCase().replace(/[^a-z\s]/g, '');

  if(PROJECT_MANAGER_MAP[emailKey]) return PROJECT_MANAGER_MAP[emailKey];
  if(PROJECT_MANAGER_MAP[nameKey]) return PROJECT_MANAGER_MAP[nameKey];

  return initials(user.name || '');
}

/** Wires header profile pill, active nav link, logout, and the collapsible sidebar. */
function initShell(activePage, user){
   // Initialize dark mode
  initTheme();
  createThemeToggle();

  const sidebarPage = ['projects', 'available-projects', 'my-projects'].includes(activePage) ? 'projects' : activePage;
  document.querySelectorAll('.nav-link').forEach(link => {
    const isProjectsGroup = link.dataset.page === 'projects' || link.getAttribute('data-projects-toggle') !== null;
    const shouldBeActive = link.dataset.page === activePage || (sidebarPage === 'projects' && isProjectsGroup);
    link.classList.toggle('active', shouldBeActive);
  });

  const nameEl = document.querySelector('[data-user-name]');
  const avatarEl = document.querySelector('[data-user-avatar]');
  if(nameEl) nameEl.textContent = user.name;
  if(avatarEl) avatarEl.textContent = initials(user.name);

  document.querySelectorAll('[data-logout]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      Store.clearSession();
      window.location.href = 'index.html';
    });
  });
  initSidebarToggle();
  initProjectsDropdown();
  const userInitials = resolveProjectManager(user);
  updateNavCounts(user.email, userInitials);
  initNotifications(user);
}

/** Desktop: collapses sidebar to an icon rail. Mobile: opens/closes an overlay drawer. */
function initSidebarToggle(){
  const shell = document.querySelector('.app-shell');
  const toggle = document.querySelector('[data-sidebar-toggle]');
  const sidebar = document.querySelector('.sidebar');
  const scrim = document.querySelector('[data-scrim]');
  if(!shell || !toggle || !sidebar) return;

  const isMobile = () => window.innerWidth <= 780;

  // Restore collapsed state on desktop.
  if(!isMobile() && localStorage.getItem(Store.SIDEBAR_KEY) === '1'){
    shell.classList.add('collapsed');
  }

  toggle.addEventListener('click', () => {
    if(isMobile()){
      const open = sidebar.classList.toggle('open');
      scrim && scrim.classList.toggle('show', open);
    }else{
      const collapsed = shell.classList.toggle('collapsed');
      localStorage.setItem(Store.SIDEBAR_KEY, collapsed ? '1' : '0');
    }
  });

  if(scrim){
    scrim.addEventListener('click', () => {
      sidebar.classList.remove('open');
      scrim.classList.remove('show');
    });
  }

  window.addEventListener('resize', () => {
    if(!isMobile()){
      sidebar.classList.remove('open');
      scrim && scrim.classList.remove('show');
    }
  });
}

function updateNavCounts(email, userInitials){
  const tasks = Store.getTasks(email);
  let filteredTasks = tasks;
  
  // If userInitials provided, filter by managed projects
  if(userInitials && typeof PROJECTS !== 'undefined'){
    const userProjects = PROJECTS.filter(p => p.projectManager === userInitials);
    const managedProjectIds = userProjects.map(p => p.id);
    filteredTasks = tasks.filter(t => managedProjectIds.includes(t.project));
  }
  
  const open = filteredTasks.filter(t => !t.done).length;
  const openCountEl = document.querySelector('[data-count="tasks"]');
  if(openCountEl) openCountEl.textContent = open;
}

function initProjectsDropdown(){
  const toggle = document.querySelector('[data-projects-toggle]');
  const submenu = document.querySelector('[data-projects-submenu]');

  if(!toggle || !submenu) return;
  if(toggle.dataset.bound === 'true') return;

  toggle.dataset.bound = 'true';
  const shouldOpen = !window.location.pathname.endsWith('tasks.html') && !window.location.pathname.endsWith('dashboard.html');
  if(shouldOpen){
    submenu.classList.add('open');
    toggle.classList.add('expanded');
  }

  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    const isOpen = submenu.classList.toggle('open');
    toggle.classList.toggle('expanded', isOpen);
  });

  const currentPage = window.location.pathname.split('/').pop();
  document.querySelectorAll('[data-submenu-page]').forEach(link => link.classList.remove('active'));

  if(currentPage === 'available-projects.html'){
    document.querySelector('[data-submenu-page="available"]')?.classList.add('active');
  } else if(currentPage === 'my-projects.html'){
    document.querySelector('[data-submenu-page="my"]')?.classList.add('active');
  }
}

function initNotifications(user){

  const headerRight = document.querySelector('.header-right');

  if(!headerRight) return;

  if(headerRight.querySelector('.notification-container')) return;

  const container = document.createElement('div');
  container.className = 'notification-container';

  container.innerHTML = `
    <button class="notification-button" type="button">
      <span class="notification-icon">🔔</span>
      <span class="notification-count" style="display:none"></span>
    </button>

    <div class="notification-box">
      <div class="notification-title">Notifications</div>
      <div class="notification-list">
        <div class="notification-empty">
          No new notifications
        </div>
      </div>
    </div>
  `;

  const profile = headerRight.querySelector('.profile-pill');

  if(profile){
    headerRight.insertBefore(container, profile);
  }else{
    headerRight.appendChild(container);
  }

  const button = container.querySelector('.notification-button');
  const box = container.querySelector('.notification-box');
  const count = container.querySelector('.notification-count');
  const list = container.querySelector('.notification-list');

  button.addEventListener('click', () => {
    box.classList.toggle('show');
  });

  const demoNotifications = [
    'Project review scheduled for Friday',
    'Team standup reminder at 2:00 PM',
    'Draft status update ready to share'
  ];

  count.textContent = demoNotifications.length;
  count.style.display = 'flex';
  list.innerHTML = demoNotifications.map(item => `<div class="notification-item">${item}</div>`).join('');
}