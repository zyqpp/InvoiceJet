// ============================================================
// InvoiceJet Design System Setup Plugin
// Uruchamia się RAZ i buduje: zmienne, style tekstu, paletę kolorów
// na stronie "🎨 Design System"
// ============================================================

(async () => {

  // ── Helpers ─────────────────────────────────────────────
  function hex(h) {
    return {
      r: parseInt(h.slice(1,3),16)/255,
      g: parseInt(h.slice(3,5),16)/255,
      b: parseInt(h.slice(5,7),16)/255
    };
  }

  async function loadFont(family, style) {
    try { await figma.loadFontAsync({ family, style }); }
    catch(e) { await figma.loadFontAsync({ family: "Roboto", style }); }
  }

  // ── 1. PRIMITIVES COLLECTION ─────────────────────────────
  const primColl = figma.variables.createVariableCollection("Primitives");
  const primModeId = primColl.modes[0].id;
  primColl.renameMode(primModeId, "Value");

  const PRIMS = [
    ["indigo/500",  "#3f51b5"],
    ["pink/A200",   "#ff4081"],
    ["red/500",     "#f44336"],
    ["slate/50",    "#f8fafc"],
    ["slate/100",   "#f1f5f9"],
    ["slate/200",   "#e2e2e2"],
    ["slate/300",   "#e5e7eb"],
    ["slate/400",   "#f0f0f0"],
    ["white",       "#ffffff"],
    ["black",       "#000000"],
    ["gray/600",    "#636363"],
    ["red/error",   "#ff0000"],
    ["orange/400",  "#ffa726"],
    ["blue/400",    "#42a5f5"],
    ["red/400",     "#ef5350"],
    ["purple/400",  "#ab47bc"],
  ];

  const primIds = {};
  for (const [name, color] of PRIMS) {
    const v = figma.variables.createVariable(name, primColl, "COLOR");
    v.setValueForMode(primModeId, hex(color));
    v.scopes = [];
    primIds[name] = v.id;
  }

  // ── 2. COLOR SEMANTIC COLLECTION ─────────────────────────
  const colorColl = figma.variables.createVariableCollection("Color");
  const colorModeId = colorColl.modes[0].id;
  colorColl.renameMode(colorModeId, "Light");

  function alias(name) {
    return { type: "VARIABLE_ALIAS", id: primIds[name] };
  }

  const SEMANTICS = [
    // surfaces
    { name: "surface/page",        alias: "slate/50",    scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "surface-page" },
    { name: "surface/card",        alias: "white",       scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "surface-card" },
    { name: "surface/dialog",      alias: "slate/50",    scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "surface-dialog" },
    { name: "surface/hover",       alias: "slate/100",   scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "surface-hover" },
    { name: "surface/subtle",      alias: "slate/400",   scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "surface-subtle" },
    { name: "surface/icon-circle", alias: "slate/200",   scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "surface-icon-circle" },
    // brand
    { name: "brand/primary",       alias: "indigo/500",  scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "brand-primary" },
    { name: "brand/accent",        alias: "pink/A200",   scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "brand-accent" },
    { name: "brand/warn",          alias: "red/500",     scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "brand-warn" },
    // text
    { name: "text/primary",        alias: "black",       scopes: ["TEXT_FILL"],                css: "text-primary" },
    { name: "text/on-primary",     alias: "white",       scopes: ["TEXT_FILL"],                css: "text-on-primary" },
    { name: "text/secondary",      alias: "gray/600",    scopes: ["TEXT_FILL"],                css: "text-secondary" },
    { name: "text/error",          alias: "red/error",   scopes: ["TEXT_FILL"],                css: "text-error" },
    // border
    { name: "border/default",      alias: "slate/300",   scopes: ["STROKE_COLOR"],             css: "border-default" },
    // status
    { name: "status/warning",      alias: "orange/400",  scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "status-warning" },
    { name: "status/info",         alias: "blue/400",    scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "status-info" },
    { name: "status/error",        alias: "red/400",     scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "status-error" },
    { name: "status/special",      alias: "purple/400",  scopes: ["FRAME_FILL","SHAPE_FILL"],  css: "status-special" },
  ];

  const colorIds = {};
  for (const s of SEMANTICS) {
    const v = figma.variables.createVariable(s.name, colorColl, "COLOR");
    v.setValueForMode(colorModeId, alias(s.alias));
    v.scopes = s.scopes;
    v.setVariableCodeSyntax("WEB", `var(--${s.css})`);
    colorIds[s.name] = v.id;
  }

  // ── 3. SPACING COLLECTION ─────────────────────────────────
  const spaceColl = figma.variables.createVariableCollection("Spacing");
  const spaceModeId = spaceColl.modes[0].id;
  spaceColl.renameMode(spaceModeId, "Value");

  const SPACING = [
    ["spacing/8",   8,  "GAP"],
    ["spacing/10",  10, "GAP"],
    ["spacing/16",  16, "GAP"],
    ["spacing/20",  20, "GAP"],
    ["spacing/24",  24, "GAP"],
    ["spacing/64",  64, "GAP"],  // navbar height
  ];

  const spaceIds = {};
  for (const [name, value, scope] of SPACING) {
    const v = figma.variables.createVariable(name, spaceColl, "FLOAT");
    v.setValueForMode(spaceModeId, value);
    v.scopes = [scope];
    v.setVariableCodeSyntax("WEB", `var(--${name.replace("/","-")})`);
    spaceIds[name] = v.id;
  }

  // ── 4. RADIUS COLLECTION ──────────────────────────────────
  const radColl = figma.variables.createVariableCollection("Radius");
  const radModeId = radColl.modes[0].id;
  radColl.renameMode(radModeId, "Value");

  const RADII = [
    ["radius/none",  0],
    ["radius/sm",    5],
    ["radius/md",    8],
    ["radius/lg",    12],
    ["radius/full",  9999],
  ];

  const radIds = {};
  for (const [name, value] of RADII) {
    const v = figma.variables.createVariable(name, radColl, "FLOAT");
    v.setValueForMode(radModeId, value);
    v.scopes = ["CORNER_RADIUS"];
    v.setVariableCodeSyntax("WEB", `var(--${name.replace("/","-")})`);
    radIds[name] = v.id;
  }

  // ── 5. TEXT STYLES ────────────────────────────────────────
  await loadFont("Inter", "Regular");
  await loadFont("Inter", "Medium");
  await loadFont("Inter", "Semi Bold");
  await loadFont("Inter", "Bold");

  const TEXT_STYLES = [
    { name: "display/h1",      size: 32, weight: "Bold",      lineH: 40 },
    { name: "display/h2",      size: 24, weight: "Bold",      lineH: 32 },
    { name: "display/h3",      size: 20, weight: "Semi Bold", lineH: 28 },
    { name: "body/large",      size: 16, weight: "Regular",   lineH: 24 },
    { name: "body/default",    size: 14, weight: "Regular",   lineH: 20 },
    { name: "body/small",      size: 12, weight: "Regular",   lineH: 16 },
    { name: "label/semibold",  size: 14, weight: "Semi Bold", lineH: 20 },
    { name: "label/medium",    size: 14, weight: "Medium",    lineH: 20 },
    { name: "stat/value",      size: 30, weight: "Semi Bold", lineH: 36 },
    { name: "stat/title",      size: 18, weight: "Regular",   lineH: 24 },
    { name: "nav/item",        size: 14, weight: "Regular",   lineH: 20 },
    { name: "nav/item-active", size: 14, weight: "Bold",      lineH: 20 },
  ];

  const styleIds = {};
  for (const s of TEXT_STYLES) {
    const style = figma.createTextStyle();
    style.name = s.name;
    style.fontName = { family: "Inter", style: s.weight };
    style.fontSize = s.size;
    style.lineHeight = { unit: "PIXELS", value: s.lineH };
    styleIds[s.name] = style.id;
  }

  // ── 6. COLOR SWATCHES ON CANVAS ──────────────────────────
  const dsPage = figma.root.children.find(p => p.name === "🎨 Design System");
  await figma.setCurrentPageAsync(dsPage);

  // Section: Color Palette
  const sectionTitle = figma.createText();
  await figma.loadFontAsync({ family: "Inter", style: "Bold" });
  sectionTitle.fontName = { family: "Inter", style: "Bold" };
  sectionTitle.characters = "Color Palette";
  sectionTitle.fontSize = 24;
  sectionTitle.x = 40;
  sectionTitle.y = 40;

  // Draw swatches row (brand + surfaces + status)
  const ALL_SWATCHES = [
    { label: "Primary",      hex: "#3f51b5" },
    { label: "Accent",       hex: "#ff4081" },
    { label: "Warn",         hex: "#f44336" },
    { label: "Surface/Page", hex: "#f8fafc" },
    { label: "Surface/Card", hex: "#ffffff" },
    { label: "Hover",        hex: "#f1f5f9" },
    { label: "Border",       hex: "#e5e7eb" },
    { label: "Icon circle",  hex: "#e2e2e2" },
    { label: "Text/2nd",     hex: "#636363" },
    { label: "Warning",      hex: "#ffa726" },
    { label: "Info",         hex: "#42a5f5" },
    { label: "Error",        hex: "#ef5350" },
    { label: "Special",      hex: "#ab47bc" },
  ];

  await figma.loadFontAsync({ family: "Inter", style: "Regular" });

  const SWATCH_W = 80, SWATCH_H = 60, GAP = 12, START_X = 40, START_Y = 90;

  for (let i = 0; i < ALL_SWATCHES.length; i++) {
    const s = ALL_SWATCHES[i];
    const x = START_X + i * (SWATCH_W + GAP);

    // Color box
    const rect = figma.createRectangle();
    rect.resize(SWATCH_W, SWATCH_H);
    rect.x = x; rect.y = START_Y;
    rect.fills = [{ type: "SOLID", color: hex(s.hex) }];
    rect.cornerRadius = 8;
    if (s.hex === "#ffffff" || s.hex === "#f8fafc" || s.hex === "#f1f5f9") {
      rect.strokes = [{ type: "SOLID", color: hex("#e5e7eb") }];
      rect.strokeWeight = 1;
    }

    // Label
    const label = figma.createText();
    label.fontName = { family: "Inter", style: "Regular" };
    label.fontSize = 10;
    label.characters = s.label;
    label.x = x; label.y = START_Y + SWATCH_H + 4;
    label.resize(SWATCH_W, 16);
    label.textAlignHorizontal = "CENTER";

    // Hex
    const hexLabel = figma.createText();
    hexLabel.fontName = { family: "Inter", style: "Regular" };
    hexLabel.fontSize = 9;
    hexLabel.characters = s.hex.toUpperCase();
    hexLabel.fills = [{ type: "SOLID", color: hex("#636363") }];
    hexLabel.x = x; hexLabel.y = START_Y + SWATCH_H + 20;
    hexLabel.resize(SWATCH_W, 14);
    hexLabel.textAlignHorizontal = "CENTER";
  }

  // Section: Spacing
  const spaceTitle = figma.createText();
  spaceTitle.fontName = { family: "Inter", style: "Bold" };
  spaceTitle.characters = "Spacing Scale";
  spaceTitle.fontSize = 24;
  spaceTitle.x = 40;
  spaceTitle.y = 220;

  const SPACINGS = [8, 10, 16, 20, 24, 64];
  for (let i = 0; i < SPACINGS.length; i++) {
    const sp = SPACINGS[i];
    const y = 260 + i * 36;
    const bar = figma.createRectangle();
    bar.resize(sp * 4, 20);
    bar.x = 120; bar.y = y;
    bar.fills = [{ type: "SOLID", color: hex("#3f51b5"), opacity: 0.3 }];
    bar.cornerRadius = 3;

    const lbl = figma.createText();
    lbl.fontName = { family: "Inter", style: "Regular" };
    lbl.fontSize = 12;
    lbl.characters = `spacing/${sp}  =  ${sp}px`;
    lbl.x = 40; lbl.y = y + 2;
  }

  // Section: Typography
  const typoTitle = figma.createText();
  typoTitle.fontName = { family: "Inter", style: "Bold" };
  typoTitle.characters = "Typography";
  typoTitle.fontSize = 24;
  typoTitle.x = 40;
  typoTitle.y = 500;

  const TYPO_SPECIMENS = [
    { label: "Display H1 — 32px Bold",     size: 32, weight: "Bold" },
    { label: "Display H2 — 24px Bold",     size: 24, weight: "Bold" },
    { label: "Display H3 — 20px Semi Bold",size: 20, weight: "Semi Bold" },
    { label: "Body Large — 16px Regular",  size: 16, weight: "Regular" },
    { label: "Body Default — 14px Regular",size: 14, weight: "Regular" },
    { label: "Body Small — 12px Regular",  size: 12, weight: "Regular" },
    { label: "Stat Value — 30px Semi Bold",size: 30, weight: "Semi Bold" },
  ];

  let typoY = 545;
  for (const t of TYPO_SPECIMENS) {
    const node = figma.createText();
    node.fontName = { family: "Inter", style: t.weight };
    node.fontSize = t.size;
    node.characters = t.label;
    node.x = 40; node.y = typoY;
    typoY += t.size + 16;
  }

  figma.closePlugin("✅ InvoiceJet Design System: zmienne, style i paleta kolorów gotowe!");
})();
