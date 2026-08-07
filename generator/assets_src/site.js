// Progressive enhancement only. Every page fully works with this file absent.

function esc(s){
  const d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML;
}

/* ---------- suggest-edit modal (used on task pages) ---------- */
function openSuggestModal(taskName){
  const overlay = document.getElementById('modalOverlay');
  if(!overlay) return;
  document.getElementById('modalTaskName').textContent = taskName;
  overlay.classList.add('show');
  const ta = document.getElementById('suggestText');
  if(ta) ta.focus();
}
function closeModal(){
  const overlay = document.getElementById('modalOverlay');
  if(overlay) overlay.classList.remove('show');
}
function submitSuggestion(){
  closeModal();
  showToast("Thanks — saved for review when community editing goes live.");
  const ta = document.getElementById('suggestText');
  if(ta) ta.value = '';
}
function showToast(msg){
  const el = document.getElementById('toast');
  if(!el) return;
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(()=>el.classList.remove('show'), 3200);
}

document.addEventListener('click', (e) => {
  const overlay = document.getElementById('modalOverlay');
  if(overlay && e.target === overlay) closeModal();
});
document.addEventListener('keydown', (e) => {
  if(e.key === 'Escape') closeModal();
});

/* ---------- client-side filter/search on browse & category pages ---------- */
(function(){
  const listArea = document.getElementById('listArea');
  if(!listArea) return; // not a browse/category page

  const searchInput = document.getElementById('searchInput');
  const chips = document.querySelectorAll('.filter-bar .chip');
  const tickets = Array.from(listArea.querySelectorAll('.ticket'));
  const countEl = document.querySelector('.section-head .count');
  const emptyTemplate = listArea.getAttribute('data-empty-html') || '';

  let activePriority = null;
  let query = '';

  function apply(){
    let visible = 0;
    tickets.forEach(t => {
      const matchesPriority = !activePriority || t.getAttribute('data-priority') === activePriority;
      const haystack = t.getAttribute('data-search') || '';
      const matchesQuery = !query || haystack.includes(query);
      const show = matchesPriority && matchesQuery;
      t.style.display = show ? '' : 'none';
      if(show) visible++;
    });
    if(countEl) countEl.textContent = countEl.getAttribute('data-total-label')
      ? `${visible} ${countEl.getAttribute('data-total-label')}`
      : `${visible} tasks`;

    let emptyEl = document.getElementById('emptyState');
    if(visible === 0){
      if(!emptyEl){
        emptyEl = document.createElement('div');
        emptyEl.id = 'emptyState';
        emptyEl.className = 'empty-state';
        emptyEl.innerHTML = '<h3>No tasks match</h3><p>Try a different search term or clear the priority filter.</p>';
        listArea.appendChild(emptyEl);
      }
    } else if(emptyEl){
      emptyEl.remove();
    }
  }

  if(searchInput){
    searchInput.addEventListener('input', (e) => {
      query = e.target.value.trim().toLowerCase();
      apply();
    });
  }

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const p = chip.getAttribute('data-priority') || null;
      activePriority = p;
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      apply();
    });
  });
})();

/* ---------- header search: jump to /browse/?q= from any page ---------- */
(function(){
  const headerSearch = document.getElementById('headerSearch');
  if(!headerSearch) return;
  headerSearch.addEventListener('keydown', (e) => {
    if(e.key === 'Enter'){
      const q = encodeURIComponent(e.target.value.trim());
      window.location.href = (window.SITE_ROOT || '') + '/browse/?q=' + q;
    }
  });
})();

// If we landed on /browse/?q=..., seed the local search box and filter.
(function(){
  const params = new URLSearchParams(window.location.search);
  const q = params.get('q');
  const searchInput = document.getElementById('searchInput');
  if(q && searchInput){
    searchInput.value = q;
    searchInput.dispatchEvent(new Event('input'));
  }
})();
