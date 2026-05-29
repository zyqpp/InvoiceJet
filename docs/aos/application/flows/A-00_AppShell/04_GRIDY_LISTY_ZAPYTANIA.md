# A-00: AppShell — Gridy, Listy, Zapytania

## Czy sekcja dotyczy tego przepływu?

> Sekcja nie dotyczy tego przepływu. AppShell nie zawiera list ani gridów danych. Zawiera statyczne drzewo nawigacji (`mat-tree`), które jest komponentem nawigacyjnym, nie tabelą danych.

## Wyjaśnienie

AppShell definiuje powłokę aplikacji i nawigację. Jego główne komponenty to:
- **NavbarComponent** — pasek nawigacyjny z przyciskami, logo, menu profilu
- **SidebarComponent** — menu boczne z drzewem nawigacji (mat-tree)
- **router-outlet** — placeholder dla zawartości ekranów

**Mat-tree w SidebarComponent** jest komponentem strukturalnym (hierarchia menu), a nie tabelą danych. Zawiera statyczne pozycje menu zdefiniowane w kodzie komponentu, a nie dane pobierane z API.

## Referencja

Jeśli szukasz grid'ów i list dla konkretnych danych:
- **A-02: Invoices** — lista faktur (grid z danymi)
- **A-06: Clients** — lista klientów (grid z danymi)
- **A-07: Products** — lista produktów (grid z danymi)
- **A-09: Bank Accounts** — lista kont bankowych (grid z danymi)
- **A-10: Document Series** — lista serii dokumentów (grid z danymi)

Te przepływy zawierać będą sekcje "Gridy, Listy, Zapytania" z mapowaniem źródeł danych, filtrów i sortowania.
