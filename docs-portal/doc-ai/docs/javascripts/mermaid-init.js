// Inicjalizacja Mermaid dla MkDocs Material
window.addEventListener("DOMContentLoaded", function () {
  if (typeof mermaid !== "undefined") {
    mermaid.initialize({
      startOnLoad: true,
      theme: "default",
      securityLevel: "loose",
      flowchart: { useMaxWidth: true, htmlLabels: true },
      sequence: { useMaxWidth: true },
    });
  }
});

// Re-inicjalizacja po nawigacji SPA (MkDocs instant loading)
document$.subscribe(function () {
  if (typeof mermaid !== "undefined") {
    mermaid.run({ querySelector: ".mermaid, code.language-mermaid" });
  }
});
