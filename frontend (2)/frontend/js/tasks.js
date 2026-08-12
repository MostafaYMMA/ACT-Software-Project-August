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
  return `
    <div class="task-row ${task.done ? 'done' : ''}" data-id="${task.id}">
      <input type="checkbox" class="stamp" ${task.done ? 'checked' : ''} aria-label="Mark task done" />
      <div class="task-main">
        <div class="task-title">${escapeHTML(task.title)}</div>
        <div class="task-meta">
          <span class="chip ${PRIORITY_CHIP[task.priority]}">${PRIORITY_LABEL[task.priority]}</span>
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

function addTask(email, {title, priority}){
  const tasks = Store.getTasks(email);
  tasks.unshift({
    id: crypto.randomUUID(),
    title,
    priority,
    done: false,
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
