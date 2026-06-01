// ============================================================
// InvoiceJet — Makieta ekranu logowania (EKRAN-01 Login)
// Uruchom: Plugins > Development > InvoiceJet Login Screen > Run
// Zgodne z tokenami z figma/design-tokens.md (1:1 z kodem)
// ============================================================

(async () => {

  // ── Helpers ────────────────────────────────────────────
  function hex(h) {
    return {
      r: parseInt(h.slice(1,3),16)/255,
      g: parseInt(h.slice(3,5),16)/255,
      b: parseInt(h.slice(5,7),16)/255
    };
  }

  async function txt(chars, opts = {}) {
    const family = opts.family || 'Inter';
    const style  = opts.style  || 'Regular';
    await figma.loadFontAsync({ family, style });
    const t = figma.createText();
    t.fontName   = { family, style };
    t.fontSize   = opts.size   || 14;
    t.characters = chars;
    t.fills      = [{ type: 'SOLID', color: opts.color || hex('#0f172a') }];
    if (opts.name) t.name = opts.name;
    return t;
  }

  // ── Znajdź lub utwórz stronę "🔐 Auth & Layout" ────────
  let authPage = figma.root.children.find(p => p.name.includes('Auth'));
  if (!authPage) {
    authPage = figma.createPage();
    authPage.name = '🔐 Auth & Layout';
  }
  await figma.setCurrentPageAsync(authPage);

  // ── Kolory 1:1 z design-tokens.md ──────────────────────
  const C = {
    primary:    hex('#3f51b5'),   // Material indigo 500
    white:      hex('#ffffff'),
    bg:         hex('#f8fafc'),   // surface/page
    border:     hex('#e5e7eb'),   // border/default
    placeholder:hex('#94a3b8'),   // muted
    textPri:    hex('#0f172a'),   // text/primary
    textSec:    hex('#636363'),   // text/secondary
    warn:       hex('#f44336'),   // Material warn
  };

  // ════════════════════════════════════════════════════════
  // FRAME GŁÓWNY  1440 × 900  (standardowy desktop viewport)
  // ════════════════════════════════════════════════════════
  const screen = figma.createFrame();
  screen.name  = 'EKRAN-01 — Login';
  screen.resize(1440, 900);
  screen.fills = [{ type: 'SOLID', color: C.bg }];
  screen.x = 100; screen.y = 100;
  authPage.appendChild(screen);

  // ════════════════════════════════════════════════════════
  // NAVBAR  1440 × 64  (navbar/height z tokenów)
  // ════════════════════════════════════════════════════════
  const navbar = figma.createFrame();
  navbar.name  = 'Navbar';
  navbar.resize(1440, 64);
  navbar.fills = [{ type: 'SOLID', color: C.primary }];
  navbar.layoutMode           = 'HORIZONTAL';
  navbar.primaryAxisAlignItems = 'CENTER';
  navbar.counterAxisAlignItems = 'CENTER';
  navbar.paddingLeft  = 40;
  navbar.paddingRight = 40;
  navbar.itemSpacing  = 0;
  navbar.primaryAxisSizingMode   = 'FIXED';
  navbar.counterAxisSizingMode   = 'FIXED';
  screen.appendChild(navbar);
  navbar.resize(1440, 64);
  navbar.layoutPositioning = 'ABSOLUTE';
  navbar.x = 0; navbar.y = 0;

  // Logo
  const logo = await txt('InvoiceJet', { family:'Inter', style:'Bold', size:20, color:C.white, name:'Logo' });
  navbar.appendChild(logo);

  // Spacer
  const spacer = figma.createFrame();
  spacer.name  = 'Spacer';
  spacer.resize(1, 1);
  spacer.fills = [];
  spacer.layoutGrow = 1;
  navbar.appendChild(spacer);
  spacer.layoutSizingHorizontal = 'FILL';

  // Nav links
  const navLinks = figma.createAutoLayout('HORIZONTAL', { name:'Nav Links', itemSpacing:24 });
  navLinks.fills             = [];
  navLinks.paddingTop        = 0; navLinks.paddingBottom = 0;
  navLinks.paddingLeft       = 0; navLinks.paddingRight  = 0;
  navbar.appendChild(navLinks);

  const lLogin    = await txt('Login',    { family:'Inter', style:'Semi Bold', size:14, color:C.white, name:'Link/Login'    });
  const lRegister = await txt('Register', { family:'Inter', style:'Regular',   size:14, color:C.white, name:'Link/Register' });
  lRegister.opacity = 0.7;
  navLinks.appendChild(lLogin);
  navLinks.appendChild(lRegister);

  // ════════════════════════════════════════════════════════
  // KARTA LOGOWANIA  (centrowana)
  // ════════════════════════════════════════════════════════
  const CARD_W = 420;

  const card = figma.createFrame();
  card.name         = 'Card/Login';
  card.fills        = [{ type: 'SOLID', color: C.white }];
  card.cornerRadius = 8;
  card.strokes      = [{ type: 'SOLID', color: C.border }];
  card.strokeWeight = 1;
  card.layoutMode   = 'VERTICAL';
  card.primaryAxisSizingMode   = 'AUTO';
  card.counterAxisSizingMode   = 'FIXED';
  card.paddingTop    = 40; card.paddingBottom = 40;
  card.paddingLeft   = 40; card.paddingRight  = 40;
  card.itemSpacing   = 24;
  screen.appendChild(card);
  card.resize(CARD_W, 10);

  // Efekt cienia
  card.effects = [{
    type: 'DROP_SHADOW',
    color: { r:0, g:0, b:0, a:0.08 },
    offset: { x:0, y:4 },
    radius: 16,
    spread: 0,
    visible: true,
    blendMode: 'NORMAL',
  }];

  // Wycentrowanie karty
  card.x = (1440 - CARD_W) / 2;
  card.y = 64 + (900 - 64 - 420) / 2;  // szacunkowe — doprecyzujemy po build

  // ── Nagłówek "Login" ─────────────────────────────────
  const heading = await txt('Login', { family:'Inter', style:'Bold', size:24, color:C.textPri, name:'Heading' });
  card.appendChild(heading);

  // ── Helper: pole formularza (label + input) ───────────
  async function makeField(labelText, placeholderText, fieldName, showEye = false) {
    const group = figma.createAutoLayout('VERTICAL', { name: `Field/${fieldName}`, itemSpacing: 8 });
    group.fills = [];
    group.paddingTop = 0; group.paddingBottom = 0;
    group.paddingLeft = 0; group.paddingRight  = 0;
    card.appendChild(group);
    group.layoutSizingHorizontal = 'FILL';

    // Label
    const label = await txt(labelText, { family:'Inter', style:'Medium', size:14, color:C.textPri, name:'Label' });
    group.appendChild(label);

    // Input wrapper
    const inputWrap = figma.createFrame();
    inputWrap.name   = 'Input';
    inputWrap.fills  = [{ type: 'SOLID', color: C.white }];
    inputWrap.strokes = [{ type: 'SOLID', color: C.border }];
    inputWrap.strokeWeight = 1;
    inputWrap.cornerRadius = 4;
    inputWrap.layoutMode   = 'HORIZONTAL';
    inputWrap.counterAxisAlignItems = 'CENTER';
    inputWrap.primaryAxisAlignItems = 'CENTER';
    inputWrap.paddingLeft  = 16; inputWrap.paddingRight  = 16;
    inputWrap.paddingTop   = 0;  inputWrap.paddingBottom = 0;
    inputWrap.itemSpacing  = 8;
    inputWrap.primaryAxisSizingMode   = 'FIXED';
    inputWrap.counterAxisSizingMode   = 'FIXED';
    group.appendChild(inputWrap);
    inputWrap.resize(CARD_W - 80, 44);   // CARD_W - 2×padding
    inputWrap.layoutSizingHorizontal = 'FILL';

    // Placeholder
    const ph = await txt(placeholderText, { family:'Inter', style:'Regular', size:14, color:C.placeholder, name:'Placeholder' });
    inputWrap.appendChild(ph);
    ph.layoutGrow = 1;
    ph.layoutSizingHorizontal = 'FILL';

    // Eye icon (password)
    if (showEye) {
      const eye = await txt('👁', { family:'Inter', style:'Regular', size:16, color:C.placeholder, name:'Eye' });
      inputWrap.appendChild(eye);
    }

    return group;
  }

  // Email
  await makeField('Email', 'pat@example.com', 'Email');

  // Password
  await makeField('Password', 'Enter your password', 'Password', true);

  // ── Przycisk Submit ───────────────────────────────────
  const btn = figma.createFrame();
  btn.name         = 'Button/Submit';
  btn.fills        = [{ type: 'SOLID', color: C.primary }];
  btn.cornerRadius = 4;
  btn.layoutMode   = 'HORIZONTAL';
  btn.primaryAxisAlignItems   = 'CENTER';
  btn.counterAxisAlignItems   = 'CENTER';
  btn.primaryAxisSizingMode   = 'FIXED';
  btn.counterAxisSizingMode   = 'FIXED';
  btn.paddingTop    = 0; btn.paddingBottom = 0;
  btn.paddingLeft   = 0; btn.paddingRight  = 0;
  card.appendChild(btn);
  btn.resize(CARD_W - 80, 44);
  btn.layoutSizingHorizontal = 'FILL';

  const btnTxt = await txt('Submit', { family:'Inter', style:'Semi Bold', size:15, color:C.white, name:'Label' });
  btn.appendChild(btnTxt);

  // ── Wycentrowanie karty po zbudowaniu ─────────────────
  const cardH = card.height;
  card.y = 64 + Math.max(40, (900 - 64 - cardH) / 2);

  // ── Screenshot ────────────────────────────────────────
  const img = await screen.screenshot();

  return {
    message: '✅ Makieta logowania gotowa!',
    screenId: screen.id,
    cardId:   card.id,
    size: `${screen.width}×${screen.height}`,
    cardSize: `${CARD_W}×${cardH}`,
    screenshot: img ? 'attached' : 'none',
    createdNodeIds: [screen.id, navbar.id, card.id],
  };

})();
