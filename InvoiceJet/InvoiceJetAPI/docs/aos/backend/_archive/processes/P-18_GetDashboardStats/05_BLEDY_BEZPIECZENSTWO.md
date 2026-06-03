# Statystyki dashboardu — Błędy i bezpieczeństwo

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |

---

## Błędy

Proces nie rzuca dedykowanych wyjątków biznesowych.

| Warunek | Status HTTP |
|---|---|
| Brak aktywnej firmy | `200 OK` z pustym `DashboardStatsDto` |
| Nieobsłużony wyjątek infrastruktury | `500 Internal Server Error` |
