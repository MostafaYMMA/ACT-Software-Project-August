/* =========================================================
   ACT — task CRUD + rendering helpers
   ========================================================= */

const PRIORITY_LABEL = { high: 'High', med: 'Medium', low: 'Low' };
const PRIORITY_CHIP  = { high: 'chip-high', med: 'chip-med', low: 'chip-low' };
const PRIORITY_ORDER = { high: 0, med: 1, low: 2 };

function relativeDay(ts){
  const days = Math.floor((Date.now() - ts) / 86400000);
  if(days <= 0) return 'today';
  if(days === 1) return 'yesterday';
  return `${days}d ago`;
}

function taskRowHTML(task){
  const status = task.status || (task.done ? 'completed' : 'active');
  const proj = task.project || '';
  return `
    <div class="task-row ${task.done ? 'done' : ''}" data-id="${task.id}" data-status="${status}">
      <button class="stamp status-${status}" aria-label="Change task status" data-status="${status}"></button>
      <div class="task-main">
        <div class="task-title">${escapeHTML(task.title)}</div>
        <div class="task-meta">
          <span class="chip ${PRIORITY_CHIP[task.priority]}">${PRIORITY_LABEL[task.priority]}</span>
          <span class="project">Project: ${escapeHTML(proj || 'No project')}</span>
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

    // status popover (handles Active / Paused / Completed)
    const stamp = row.querySelector('.stamp');
    stamp.addEventListener('click', (e) => {
      e.stopPropagation();
      const currentStatus = row.dataset.status || 'active';
      createStatusPopover(stamp, currentStatus, (newStatus) => {
        const tasks = Store.getTasks(email);
        const t = tasks.find(t => t.id === id);
        if(!t) return;
        t.status = newStatus;
        t.done = (newStatus === 'completed');
        Store.saveTasks(email, tasks);
        // update DOM
        row.dataset.status = newStatus;
        row.classList.toggle('done', t.done);
        stamp.classList.remove('status-active','status-paused','status-completed');
        stamp.classList.add(`status-${newStatus}`);
        onChange && onChange();
      });
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

/** Create a small status popover next to target element. Calls `onSelect(status)` when chosen. */
function createStatusPopover(target, currentStatus, onSelect){
  // remove any existing popover
  const existing = document.querySelector('.status-popover');
  if(existing) existing.remove();

  const pop = document.createElement('div');
  pop.className = 'status-popover';
  pop.innerHTML = `
    <button class="status-option" data-value="active"><span class="dot dot-active"></span>Active</button>
    <button class="status-option" data-value="paused"><span class="dot dot-paused"></span>Paused</button>
    <button class="status-option" data-value="completed"><span class="dot dot-completed">✓</span>Completed</button>
  `;
  document.body.appendChild(pop);

  // position near the target
  const rect = target.getBoundingClientRect();
  pop.style.top = `${rect.top + window.scrollY + (rect.height/2) - 28}px`;
  pop.style.left = `${rect.right + 12 + window.scrollX}px`;

  // animation show
  requestAnimationFrame(() => pop.classList.add('show'));

  function cleanup(){
    pop.remove();
    document.removeEventListener('click', onDocClick, true);
  }

  function onDocClick(ev){
    if(!pop.contains(ev.target) && ev.target !== target) cleanup();
  }
  document.addEventListener('click', onDocClick, true);

  pop.querySelectorAll('.status-option').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const val = btn.dataset.value;
      onSelect(val);
      cleanup();
    });
  });
}

function addTask(email, {title, priority}){
  const tasks = Store.getTasks(email);
  tasks.unshift({
    id: crypto.randomUUID(),
    title,
    priority,
    done: false,
    status: 'active',
    project: '',
    createdAt: Date.now()
  });
  Store.saveTasks(email, tasks);
}

function taskStats(email){
  const tasks = Store.getTasks(email);
  const done = tasks.filter(t => t.done).length;
  const open = tasks.length - done;
  const byPriority = { high: 0, med: 0, low: 0 };
  tasks.forEach(t => { if(!t.done) byPriority[t.priority]++; });
  const completion = tasks.length ? Math.round((done / tasks.length) * 100) : 0;
  return { total: tasks.length, done, open, byPriority, completion };
}
