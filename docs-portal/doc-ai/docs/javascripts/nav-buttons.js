/**
 * InvoiceJet Docs — Przyciski kategorii w lewym sidebarze
 * Wstrzykuje panel z przyciskami nad drzewem nawigacji.
 * Każdy przycisk prowadzi do folderu głównego i podświetla się gdy jesteś w środku.
 */

const CATEGORIES = [
  { id: "root",    icon: "🏠", label: "doc_AI (główna)",          path: "README.html" },
  { id: "meta",    icon: "📋", label: "00_meta — Metadokumenty",  path: "00_meta/README.html" },
  { id: "ekrany",  icon: "🖥️", label: "01_ekrany — Ekrany",       path: "01_ekrany/README.html" },
  { id: "procesy", icon: "⚙️", label: "02_procesy — Procesy",     path: "02_procesy/README.html" },
  { id: "alg",     icon: "🔧", label: "03_algorytmy",              path: "03_algorytmy/README.html" },
  { id: "api",     icon: "🔌", label: "04_api — API i integracje", path: "04_api_i_integracje/README.html" },
  { id: "model",   icon: "🗄️", label: "05_model_danych",          path: "05_model_danych/README.html" },
  { id: "role",    icon: "🔐", label: "06_role_i_uprawnienia",     path: "06_role_i_uprawnienia/README.html" },
  { id: "uc",      icon: "📐", label: "07_use_case",               path: "07_use_case/README.html" },
  { id: "biz",     icon: "🏢", label: "08_model_biznesowy",        path: "08_model_biznesowy/README.html" },
  { id: "bp",      icon: "🔄", label: "09_procesy_biznesowe",      path: "09_procesy_biznesowe/README.html" },
  { id: "testy",   icon: "✅", label: "10_testy",                  path: "10_testy/README.html" },
  { id: "mapy",    icon: "🗺️", label: "_mapowania",                path: "_mapowania/README.html" },
  { id: "slow",    icon: "📖", label: "_slowniki",                 path: "_slowniki/README.html" },
];

function buildCategoryPanel() {
  const sidebar = document.querySelector(".md-sidebar--primary .md-sidebar__scrollwrap");
  if (!sidebar || document.getElementById("nav-cat-panel")) return;

  const currentPath = window.location.pathname;

  // ── Przełącznik portali ──
  const switchHtml = `
    <div class="portal-switch" id="portal-switch">
      <a href="http://127.0.0.1:8001/" class="current" title="Dokumentacja Techniczna">📚 Techniczna</a>
      <a href="http://127.0.0.1:8002/" title="Dokumentacja Użytkownika">👤 Użytkownik</a>
    </div>`;

  // ── Panel kategorii ──
  const items = CATEGORIES.map(cat => {
    const isActive = currentPath.includes("/" + cat.id + "/") ||
                     (cat.id === "root" && !CATEGORIES.slice(1).some(c => currentPath.includes("/" + c.id + "/")));
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
      <span class="nav-categories__title">Kategorie</span>
      <ul class="nav-cat-btn-list" style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1px;">
        ${items}
      </ul>
    </div>`;

  sidebar.insertBefore(panel, sidebar.firstChild);
}

// Uruchom po załadowaniu strony (MkDocs instant navigation)
function init() {
  buildCategoryPanel();
}

document.addEventListener("DOMContentLoaded", init);

// Obsługa MkDocs instant navigation (SPA)
if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    const existing = document.getElementById("nav-cat-panel");
    if (existing) existing.remove();
    buildCategoryPanel();
  });
} else {
  // Fallback: obserwuj zmiany URL
  let lastUrl = location.href;
  new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
      lastUrl = url;
      const existing = document.getElementById("nav-cat-panel");
      if (existing) existing.remove();
      setTimeout(buildCategoryPanel, 100);
    }
  }).observe(document, { subtree: true, childList: true });
}
