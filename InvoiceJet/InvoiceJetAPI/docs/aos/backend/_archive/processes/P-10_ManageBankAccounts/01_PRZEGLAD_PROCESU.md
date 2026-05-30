# Zarządzanie kontami bankowymi — Przegląd procesu

## Cel

Proces obsługuje listowanie, dodawanie, edycję i usuwanie kont bankowych aktywnej firmy użytkownika. Logika gwarantuje, że aktywne konto (`IsActive = true`) dezaktywuje pozostałe konta tej samej firmy.

---

## Diagram

```mermaid
flowchart TD
  A["GET konta"] --> B["GetUserFirmBankAccounts()"]
  C["POST konto"] --> D["AddUserFirmBankAccount()"]
  D --> E["DeactivateOtherBankAccounts() gdy IsActive=true"]
  F["PUT konto"] --> G["EditUserFirmBankAccount()"]
  G --> H["DeactivateOtherBankAccounts(excludeId) gdy IsActive=true"]
  I["PUT usuwanie"] --> J["DeleteUserFirmBankAccounts()"]
```
