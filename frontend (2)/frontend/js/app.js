/* =========================================================
   ACT — shared app utilities
   Demo-only auth: users + sessions live in localStorage.
   Swap Store.* for real API calls when a backend exists.
   ========================================================= */

const Store = {
  USERS_KEY: 'act_users',
  SESSION_KEY: 'act_session',
  SIDEBAR_KEY: 'act_sidebar_collapsed',

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
      { id: crypto.randomUUID(), title: 'Wireframe the onboarding flow', priority: 'high', done: false, status: 'active', project: 'OSMO Website', createdAt: now - 86400000 * 2 },
      { id: crypto.randomUUID(), title: 'Review pull request #114',      priority: 'med',  done: false, status: 'active', project: 'ACT Dashboard', createdAt: now - 86400000 },
      { id: crypto.randomUUID(), title: 'Write weekly status update',    priority: 'low',  done: true,  status: 'completed', project: 'Internal', createdAt: now - 86400000 * 3 },
      { id: crypto.randomUUID(), title: 'Sync with design on sidebar UI', priority: 'med', done: true,  status: 'completed', project: 'OSMO Website', createdAt: now - 86400000 * 4 },
    ]);
  }
};

/** Redirect to login if no session; call at top of protected pages. */
function requireAuth(){
  const user = Store.currentUser();
  if(!user){
    window.location.href = 'index.html';
    return null;
  }
  Store.seedTasksIfEmpty(user.email);
  return user;
}

function initials(name){
  return name.trim().split(/\s+/).slice(0,2).map(p => p[0].toUpperCase()).join('');
}

/** Wires header profile pill, active nav link, logout, and the collapsible sidebar. */
function initShell(activePage, user){
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.toggle('active', link.dataset.page === activePage);
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
  updateNavCounts(user.email);
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

function updateNavCounts(email){
  const tasks = Store.getTasks(email);
  const open = tasks.filter(t => !t.done).length;
  const openCountEl = document.querySelector('[data-count="tasks"]');
  if(openCountEl) openCountEl.textContent = open;
}
