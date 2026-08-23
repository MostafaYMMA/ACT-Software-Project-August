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

// ===== PM Work Hours Calendar (placeholder data) =====
const pmNames = ['Sara Ahmed', 'Omar Khaled', 'Mona Adel'];
let pmCalDate = new Date();
pmCalDate.setDate(1);

const pmMonthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const pmWeekdayNames = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

const pmWeekdaysEl = document.getElementById('pm-cal-weekdays');
if(pmWeekdaysEl){
  pmWeekdaysEl.innerHTML = pmWeekdayNames.map(w => `<div>${w}</div>`).join('');

  function pmHoursForDay(date){
    const day = date.getDate();
    const isWeekend = date.getDay() === 5 || date.getDay() === 6; // Fri & Sat
    return pmNames.map((name, i) => {
      if(isWeekend) return { name, hours: 0 };
      const seed = (day * (i + 3) * 7) % 9;
      const hours = 2 + (seed % 7);
      return { name, hours };
    });
  }

  function showPmDay(dateObj){
    const panel = document.getElementById('pm-day-panel');
    const label = dateObj.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    const rows = pmHoursForDay(dateObj);
    const total = rows.reduce((sum, r) => sum + r.hours, 0);

    panel.innerHTML = `
      <div style="font-weight:700; margin-bottom:10px;">${label} — ${total}h total</div>
      ${rows.map(r => `
        <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed var(--color-line);">
          <div style="font-size:14px;">${r.name}</div>
          <div style="font-size:13px; color:var(--color-primary-darker); font-weight:600;">${r.hours}h</div>
        </div>
      `).join('')}
    `;
    panel.style.display = 'block';
  }

  function renderPmCalendar(){
    const year = pmCalDate.getFullYear();
    const month = pmCalDate.getMonth();

    document.getElementById('pm-cal-title').textContent = `${pmMonthNames[month]} ${year} — PM Hours`;

    const firstDay = new Date(year, month, 1);
    const startOffset = firstDay.getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const today = new Date();
    today.setHours(0,0,0,0);

    let cells = '';
    for(let i = 0; i < startOffset; i++){
      cells += `<div></div>`;
    }

    for(let day = 1; day <= daysInMonth; day++){
      const cellDate = new Date(year, month, day);
      cellDate.setHours(0,0,0,0);
      const isToday = cellDate.getTime() === today.getTime();
      const rows = pmHoursForDay(cellDate);
      const total = rows.reduce((sum, r) => sum + r.hours, 0);

      cells += `
        <div class="pm-day-cell" data-date="${cellDate.getTime()}" style="min-height:60px; border-radius:8px; background:var(--color-line); padding:6px; display:flex; flex-direction:column; justify-content:space-between; cursor:pointer; ${isToday ? 'outline:2px solid var(--color-primary);' : ''}">
          <div style="font-size:12px; color:var(--color-ink-soft);">${day}</div>
          <div style="align-self:flex-end; font-size:11px; font-weight:700; color:${total > 0 ? 'var(--color-primary-darker)' : 'var(--color-ink-soft)'};">${total > 0 ? total + 'h' : '—'}</div>
        </div>
      `;
    }

    const gridEl = document.getElementById('pm-cal-grid');
    gridEl.innerHTML = cells;

    gridEl.querySelectorAll('.pm-day-cell').forEach(cell => {
      cell.addEventListener('click', () => {
        showPmDay(new Date(Number(cell.dataset.date)));
      });
    });
  }

  document.getElementById('pm-cal-prev').addEventListener('click', () => {
    pmCalDate.setMonth(pmCalDate.getMonth() - 1);
    renderPmCalendar();
  });
  document.getElementById('pm-cal-next').addEventListener('click', () => {
    pmCalDate.setMonth(pmCalDate.getMonth() + 1);
    renderPmCalendar();
  });
  document.getElementById('pm-cal-today').addEventListener('click', () => {
    pmCalDate = new Date();
    pmCalDate.setDate(1);
    renderPmCalendar();
  });

  renderPmCalendar();
}

// ===== Notifications dropdown =====
document.addEventListener('DOMContentLoaded', () => {
  const notifBtn = document.getElementById('notifBtn');
  const notifBox = document.getElementById('notifBox');
  if (!notifBtn || !notifBox) return;

  notifBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    notifBox.classList.toggle('show');
  });

  document.addEventListener('click', (e) => {
    if (!notifBox.contains(e.target) && !notifBtn.contains(e.target)) {
      notifBox.classList.remove('show');
    }
  });
});

function addNotification(text){
  const list = document.getElementById('notifList');
  if (!list) return;
  const empty = list.querySelector('.notification-empty');
  if (empty) empty.remove();

  const item = document.createElement('div');
  item.className = 'notification-item';
  item.textContent = text;
  list.prepend(item);

  const countEl = document.getElementById('notifCount');
  const current = parseInt(countEl.textContent || '0', 10) + 1;
  countEl.textContent = current;
  countEl.classList.add('show');

}