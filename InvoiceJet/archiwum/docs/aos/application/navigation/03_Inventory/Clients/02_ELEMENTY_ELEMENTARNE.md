# Clients - Elementy elementarne

| Element | Typ | Komponent | Opis |
|---|---|---|---|
| Lista klientow | ekran | `ClientsComponent` | Grid firm oznaczonych jako klienci. |
| Dialog klienta | dialog | `AddEditClientDialogComponent` | Dodanie albo edycja firmy klienta. |
| Pobranie ANAF | operacja | `FirmService.getFirmFromAnaf()` | Uzupelnienie danych firmy po CUI. |
| Usuwanie | operacja masowa | `deleteSelected()` | Usuwa zaznaczone firmy. |
