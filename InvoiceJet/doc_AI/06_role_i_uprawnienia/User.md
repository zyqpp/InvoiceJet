# Rola: User

| Atrybut | Wartość |
|---|---|
| ID | ROLA-01 |
| Nazwa | `User` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Jedyna rola w systemie InvoiceJet. Reprezentuje zalogowanego użytkownika końcowego.

## Nadawanie roli

Rola nadawana automatycznie przy rejestracji:
```csharp
// AuthService.cs › RegisterUser
var user = new User { ..., Role = "User" };
```

Zapisywana w kolumnie `User.Role` (typ `nvarchar(max)`).

## JWT Token

Rola zapisana jako claim:
```csharp
new(ClaimTypes.Role, "User")
```

## Uprawnienia

| Zasoby | Operacje |
|---|---|
| Własna firma | Dodaj, edytuj, wyświetl |
| Firmy klientów | Dodaj, edytuj, wyświetl listę, usuń |
| Konta bankowe | CRUD |
| Produkty | CRUD |
| Serie dokumentów | CRUD |
| Dokumenty | CRUD + TransformToStorno + PDF |
| Dashboard | Odczyt statystyk |
| Integracja ANAF | Odczyt danych firmy |

**Uwaga:** Każdy user widzi wyłącznie swoje zasoby (izolacja przez `userFirmId` z JWT).

## Ekrany dostępne

Wszystkie ekrany po zalogowaniu (`/dashboard/**`):

| Ekran | Trasa |
|---|---|
| Dashboard | `/dashboard` |
| Dane firmy | `/dashboard/firm-details` |
| Klienci | `/dashboard/clients` |
| Konta bankowe | `/dashboard/bank-accounts` |
| Produkty | `/dashboard/products` |
| Serie dokumentów | `/dashboard/document-series` |
| Faktury | `/dashboard/invoices` |
| Proformy | `/dashboard/invoice-proformas` |
| Storna | `/dashboard/invoice-stornos` |
| Formularz faktury | `/dashboard/add-invoice`, `/dashboard/edit-invoice/:id` |
| Formularz proformy | `/dashboard/add-invoice-proforma`, `/dashboard/edit-invoice-proforma/:id` |
| Formularz storno | `/dashboard/edit-invoice-storno/:id` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
