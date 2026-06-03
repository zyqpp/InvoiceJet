# Serie dokumentów (Document Series)

![Lista serii dokumentów](../assets/screens/serie_dokumentow.png)

## Co to jest?
Ekran do zarządzania numeracją dokumentów. Seria definiuje, jak będą numerowane Twoje faktury — np. „FV/2024/001", „FV/2024/002" itd.

> ⚠️ **Wymagane przed pierwszą fakturą.** Bez skonfigurowanej serii nie możesz wystawić dokumentu.

---

## Kolumny tabeli

| Kolumna | Co pokazuje |
|---|---|
| ☐ | Zaznaczanie do operacji masowych |
| **Document Type** | Typ: [Faktura](10_faktury.md) / [Proforma](11_proformy.md) / [Storno](12_storna.md) |
| **Series Name** | Prefiks numeru (np. „FV/2024/") |
| **First Number** | Numer startowy |
| **Current Number** | Aktualny numer (rośnie automatycznie) |
| **Is Default** | Czy seria jest domyślna dla danego typu |

---

## Co możesz zrobić?

### Dodanie serii
Kliknij **Add Document Series** — otworzy się okno dialogowe.

**Pola formularza serii:**

| Pole | Opis |
|---|---|
| **Document Type** | Typ dokumentu: Faktura, Proforma lub Storno |
| **Series Name** | Prefiks numeru (np. „FV/2024/", „PRO/") |
| **First Number** | Od jakiego numeru zacząć (zwykle `1`) |

### Edycja serii
Kliknij na wiersz serii — otworzy się formularz edycji.

### Usunięcie serii
1. Zaznacz serie (☐)
2. Kliknij **Delete**

---

## Ważne informacje
- Zalecane: oddzielna seria dla każdego typu dokumentu
- Możesz mieć kilka serii dla tego samego typu (np. różne lata)
- Numer bieżący rośnie automatycznie — nie musisz go pilnować
- Przy wystawianiu dokumentu wybierasz serię z listy

---

📖 Instrukcja krok po kroku: [P-05b Konfiguracja serii dokumentów](../02_procesy/P-05b_konfiguracja_serii.md)

🔗 Powiązane: [Faktury](10_faktury.md) · [Proformy](11_proformy.md) · [Storna](12_storna.md)
