const adminTitles = {
  dashboard: 'Admin dashboard',
  'project-managers': 'View Project Managers',
  projects: 'View All Projects',
  approvals: 'Project Manager Approve',
  settings: 'Settings'
};

const adminShell = document.querySelector('.admin-interface .app-shell');
const adminTitle = document.getElementById('page-title');
const adminSidebar = document.querySelector('.admin-interface .sidebar');
const adminScrim = document.querySelector('.admin-interface [data-scrim]');
const adminThemeToggle = document.querySelector('.admin-interface .theme-toggle');

function updateAdminThemeButton(){
  adminThemeToggle.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
}

adminThemeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  localStorage.setItem('act_theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
  updateAdminThemeButton();
});

updateAdminThemeButton();

function setAdminSection(section){
  const selectedSection = adminTitles[section] ? section : 'dashboard';
  document.querySelectorAll('[data-section]').forEach(link => {
    link.classList.toggle('active', link.dataset.section === selectedSection);
  });
  document.querySelectorAll('[data-panel]').forEach(panel => {
    panel.classList.toggle('active', panel.dataset.panel === selectedSection);
  });
  adminTitle.textContent = adminTitles[selectedSection];
  history.replaceState(null, '', `#${selectedSection}`);
}

document.querySelectorAll('[data-section]').forEach(link => {
  link.addEventListener('click', () => setAdminSection(link.dataset.section));
});

document.querySelector('[data-sidebar-toggle]').addEventListener('click', () => {
  if(window.innerWidth <= 780){
    const isOpen = adminSidebar.classList.toggle('open');
    adminScrim.classList.toggle('show', isOpen);
    return;
  }
  adminShell.classList.toggle('collapsed');
});

adminScrim.addEventListener('click', () => {
  adminSidebar.classList.remove('open');
  adminScrim.classList.remove('show');
});

window.addEventListener('resize', () => {
  if(window.innerWidth > 780){
    adminSidebar.classList.remove('open');
    adminScrim.classList.remove('show');
  }
});

function closeModal(modal){
  modal.hidden = true;
  modal.querySelectorAll('.form-status').forEach(status => {
    status.textContent = '';
    status.className = 'form-status';
  });
}

document.querySelectorAll('[data-modal-open]').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelector(`[data-modal="${button.dataset.modalOpen}"]`).hidden = false;
  });
});

document.querySelectorAll('[data-modal-close]').forEach(button => {
  button.addEventListener('click', () => closeModal(button.closest('[data-modal]')));
});

document.querySelectorAll('.admin-modal-backdrop').forEach(backdrop => {
  backdrop.addEventListener('click', event => {
    if(event.target === backdrop) closeModal(backdrop);
  });
});

document.querySelector('[data-form="password"]').addEventListener('submit', event => {
  event.preventDefault();
  const form = event.currentTarget;
  const status = form.querySelector('[data-form-status]');
  const newPassword = form.querySelector('#new-password').value;
  const confirmPassword = form.querySelector('#confirm-password').value;
  if(newPassword !== confirmPassword){
    status.textContent = 'New passwords do not match.';
    status.className = 'form-status show err';
    return;
  }
  status.textContent = 'Password service is not connected yet. No changes were made.';
  status.className = 'form-status show err';
});

document.querySelector('[data-form="admin"]').addEventListener('submit', event => {
  event.preventDefault();
  const form = event.currentTarget;
  const status = form.querySelector('[data-form-status]');
  if(!form.checkValidity()){
    form.reportValidity();
    return;
  }
  status.textContent = 'Admin account service is not connected yet. No account was created.';
  status.className = 'form-status show err';
});

setAdminSection(window.location.hash.slice(1) || 'dashboard');
