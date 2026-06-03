# InvoiceJet — Tokeny designu (źródło: KOD, 1:1)

> **Po co ten plik:** to jest skompresowane źródło prawdy dla wyglądu. Agent budujący
> Figmę czyta TEN plik zamiast re-skanować 23 pliki SCSS. Oszczędza tokeny i gwarantuje
> spójność 1:1 z aplikacją.
>
> **Skąd pochodzą wartości:** `InvoiceJetUI/angular.json` (motyw Material) +
> `src/styles.scss` (globalne) + SCSS komponentów. Motyw bazowy = **JASNY**
> (domyślne tło `#f8fafc`). Wartości ciemnego motywu są spisane tylko referencyjnie —
> NIE budujemy ich teraz.
>
> Aby odświeżyć po zmianach w kodzie: `figma/scripts/extract-tokens.ps1`.

## 1. Motyw Material (prebuilt: `indigo-pink`)

Źródło: `angular.json` → `@angular/material/prebuilt-themes/indigo-pink.css`.

| Rola | Hex | Uwaga |
|---|---|---|
| Primary (indigo 500) | `#3f51b5` | główne przyciski, akcenty, linki |
| Primary contrast | `#ffffff` | tekst na primary |
| Accent (pink A200) | `#ff4081` | FAB / akcent |
| Warn (red 500) | `#f44336` | błędy / usuwanie |

## 2. Kolory — motyw JASNY (bazowy)

### Powierzchnie
| Token | Hex | Użycie |
|---|---|---|
| `surface/page` | `#f8fafc` | tło strony (`html, body`) |
| `surface/card` | `#ffffff` | karty, toolbar, tabele |
| `surface/dialog` | `#f8fafc` | tło modali (`.dialog-card`) |
| `surface/hover` | `#f1f5f9` | hover/active w sidebarze |
| `surface/subtle` | `#f0f0f0` | tło kontenera sidenav |
| `surface/icon-circle` | `#e2e2e2` | tło ikon w kartach dashboardu |

### Linie / obramowania
| Token | Hex | Użycie |
|---|---|---|
| `border/default` | `#e5e7eb` | obramowania tabel/sekcji |

### Tekst
| Token | Wartość | Użycie |
|---|---|---|
| `text/primary` | `rgba(0,0,0,0.87)` | domyślny tekst Material |
| `text/secondary` | `#636363` | nagłówki/ikony kart dashboardu |
| `text/error` | `red` (`#ff0000`) | `.p-error` |

### Statusy (toasty `ngx-toastr`)
| Token | Hex | Znaczenie |
|---|---|---|
| `status/warning` | `#ffa726` | 400 Bad Request |
| `status/info` | `#42a5f5` | 404 Not Found |
| `status/error` | `#ef5350` | 500 Server Error |
| `status/special` | `#ab47bc` | błąd nieoczekiwany |

## 3. Kolory — motyw CIEMNY (referencja, NIE budujemy teraz)
`bg/deep #0f172a` · `surface #1e293b` · `text #ffffff` · `muted #94a3b8`.
Aktywowany klasą `body.dark-mode`.

## 4. Typografia
- **Rodzina:** `Inter` (Google Fonts, wagi 100–900), fallback `sans-serif`. Ładowana globalnie, nadpisuje domyślny Roboto Material.
- **Wagi w użyciu:** 400 (regular), 600 (`.fullName`), bold (`.active-link`).
- **Rozmiary jawne w kodzie (dashboard):** tytuł karty `18px`, wartość statystyki `30px`, ikona `24px`.
- Pozostała skala = domyślna typografia Angular Material (`mat-typography`).

## 5. Odstępy i wymiary
| Token | Wartość | Źródło |
|---|---|---|
| `space/base` | `8px` | jednostka bazowa |
| skala | `8 · 10 · 16 · 20 · 24` | wartości realnie używane |
| `container/padding` | `24px` | `.container`, `.inner-container` |
| `container/max-width` | `1240px` | `.container` |
| `navbar/height` | `64px` | `calc(100vh - 64px)` |
| `sidebar/width` | `300px` | `mat-sidenav` |
| `sidebar/padding` | `20px` | `mat-sidenav` |
| `form/max-width` | `500px` | formularze (login) |
| `grid/gap` | `16px` | siatka kart dashboardu |
| `avatar/size` | `40px` | przycisk profilu (koło) |
| `radius/sm` | `5px` | węzły nawigacji |
| `radius/full` | `50%` | awatary, ikony kołowe |

## 6. Layout — kluczowe układy
- **Navbar:** `mat-toolbar`, `justify-content: space-between`, awatar 40px (koło, białe tło, czarna litera) po prawej.
- **Sidebar:** `mat-tree` nawigacja, szerokość 300px, węzeł aktywny = tło `#f1f5f9` + bold, radius 5px.
- **Dashboard — siatka kart statystyk (responsywna):**
  - ≥1200px → 4 kolumny · 900–1199px → 3 · 600–899px → 2 · <600px → 1
  - Karta: ikona w kole (`#e2e2e2`, padding 10px) NAD tytułem (`column-reverse`), tytuł 18px `#636363`, wartość 30px.
- **Listy:** tabela `mat-table` w karcie białej, nagłówek sekcji `padding: 16px 24px`, `space-between` (tytuł + przycisk „Add").

## 7. Ikony
Material Icons (`mat-icon`). W Figmie użyć pluginu „Material Symbols / Material Icons" lub biblioteki ikon Material.
