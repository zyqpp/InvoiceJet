window.addEventListener("DOMContentLoaded", function () {
  if (typeof mermaid !== "undefined") {
    mermaid.initialize({ startOnLoad: true, theme: "default", securityLevel: "loose" });
  }
});

document$.subscribe(function () {
  if (typeof mermaid !== "undefined") {
    mermaid.run({ querySelector: ".mermaid, code.language-mermaid" });
  }
});
