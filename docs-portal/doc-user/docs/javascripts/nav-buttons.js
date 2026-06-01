/**
 * InvoiceJet Docs User — Przyciski kategorii w lewym sidebarze
 */

const CATEGORIES = [
  { id: "root",    icon: "🏠", label: "Strona główna",       path: "README.html" },
  { id: "ekrany",  icon: "🖥️", label: "Opisy ekranów",       path: "01_ekrany/README.html" },
  { id: "procesy", icon: "▶️", label: "Instrukcje procesów", path: "02_procesy/README.html" },
  { id: "zrodla",  icon: "📚", label: "Źródła",              path: "zrodla.html" },
];

function buildCategoryPanel() {
  const sidebar = document.querySelector(".md-sidebar--primary .md-sidebar__scrollwrap");
  if (!sidebar || document.getElementById("nav-cat-panel")) return;

  const currentPath = window.location.pathname;

  const switchHtml = `
    <div class="portal-switch" id="portal-switch">
      <a href="http://127.0.0.1:8001/" title="Dokumentacja Techniczna">📚 Techniczna</a>
      <a href="http://127.0.0.1:8002/" class="current" title="Dokumentacja Użytkownika">👤 Użytkownik</a>
    </div>`;

  const items = CATEGORIES.map(cat => {
    const isActive = cat.id === "root"
      ? !["ekrany","procesy","zrodla"].some(c => currentPath.includes("/" + c))
      : currentPath.includes("/" + cat.id);
    return `
      <li>
        <a href="${cat.path}"
           class="nav-cat-btn${isActive ? " active" : ""}"
           data-cat="${cat.id}"
           title="${cat.label}">
          <span class="cat-icon">${cat.icon}</span>
          <span class="cat-label">${cat.label}</span>
        </a>
      </li>`;
  }).join("");

  const panel = document.createElement("div");
  panel.id = "nav-cat-panel";
  panel.innerHTML = `
    ${switchHtml}
    <div class="nav-categories">
      <span class="nav-categories__title">Sekcje</span>
      <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1px;">
        ${items}
      </ul>
    </div>`;

  sidebar.insertBefore(panel, sidebar.firstChild);
}

document.addEventListener("DOMContentLoaded", buildCategoryPanel);

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    const existing = document.getElementById("nav-cat-panel");
    if (existing) existing.remove();
    buildCategoryPanel();
  });
}
