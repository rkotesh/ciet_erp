/* ============================================================
   FACULTY HUB — GLOBAL SCRIPTS
   ============================================================ */

// Custom cursor removed: using normal system cursor.

// ── Theme Management (Removed) ───────────────────────────────
document.documentElement.classList.remove('dark');
document.body.classList.remove('dark');
document.documentElement.setAttribute('data-bs-theme', 'light');

// ── Sidebar Logic ────────────────────────────────────────────
const sidebar      = document.getElementById('app-sidebar');
const mainContent  = document.querySelector('.main-content');
const toggleBtn    = document.getElementById('sidebar-toggle');

// Create overlay for mobile
const overlay = document.createElement('div');
overlay.className = 'sidebar-overlay';
document.body.appendChild(overlay);

function openSidebar() {
    if (!sidebar) return;
    sidebar.classList.add('sidebar-open');
    if (mainContent) mainContent.classList.add('sidebar-open');
    overlay.classList.add('active');
}

function closeSidebar() {
    if (!sidebar) return;
    sidebar.classList.remove('sidebar-open');
    if (mainContent) mainContent.classList.remove('sidebar-open');
    overlay.classList.remove('active');
}

if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.contains('sidebar-open') ? closeSidebar() : openSidebar();
    });
}

overlay.addEventListener('click', closeSidebar);

// Close sidebar on ESC
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSidebar();
});

// ── Logout Handler ───────────────────────────────────────────
document.querySelectorAll('.logout').forEach(btn => {
    btn.addEventListener('click', e => {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
            // In a real app: window.location.href = 'login.html';
            alert('Logging out…');
        }
    });
});

// ── Global State (stub) ──────────────────────────────────────
const globalState = {
    deptFilter: 'all',
    yearFilter: 0
};
