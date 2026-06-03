# Faktury korygujące — storno (Invoice Stornos)

![Lista storn — wygląd identyczny z listą faktur](../assets/screens/faktury.png)

> Ekran storn wygląda identycznie jak [lista faktur](10_faktury.md) — te same kolumny i układ. Różnica: brak przycisku „Transform to Storno".

## Co to jest?
Lista faktur korygujących. Faktura korygująca wystawiana jest, gdy trzeba anulować lub poprawić wcześniej wystawioną [fakturę](10_faktury.md) — np. w przypadku błędu lub zwrotu towaru.

---

> ⚠️ **Nowego storna nie można dodać ręcznie z tego ekranu.**
> Storno tworzy się wyłącznie przez opcję **„Transform to Storno"** na liście [Faktur](10_faktury.md).
> → [Jak wystawić fakturę korygującą](../02_procesy/P-07_faktura_korygujaca.md)

---

## Kolumny tabeli

| Kolumna | Co pokazuje |
|---|---|
| ☐ | Zaznaczanie |
| **Document Number** | Numer storna |
| **Client Name** | Kontrahent → [Klienci](06_klienci.md) |
| **Issue Date** | Data wystawienia |
| **Due Date** | Termin |
| **Total Value** | Wartość brutto |
| **Status** | **Unpaid** / **Paid** |

---

## Co możesz zrobić?

| Akcja | Jak |
|---|---|
| **Przeglądanie** | Przewijaj listę, klikaj nagłówki kolumn żeby sortować |
| **Edycja storna** | Kliknij na wiersz → [Formularz](10b_formularz_faktury.md) |
| **Usunięcie** | Zaznacz (☐) → **Delete** |
| **PDF** | Z [formularza](10b_formularz_faktury.md) → Preview PDF / Generate PDF |

---

## Jak powstaje storno?

1. Przejdź do [Faktury](10_faktury.md)
2. Zaznacz fakturę do skorygowania (☐)
3. Kliknij **Transform to Storno**
4. Aplikacja automatycznie tworzy dokument korygujący
5. Pojawia się na tej liście — możesz go teraz edytować

---

## Ważne informacje
- Oryginalna faktura pozostaje na liście [Faktur](10_faktury.md) — nie jest usuwana
- Storno **nie dotyczy proform** — tę opcję mają wyłącznie faktury zwykłe

---

📖 Instrukcja krok po kroku: [P-07 Faktura korygująca (storno)](../02_procesy/P-07_faktura_korygujaca.md)

🔗 Powiązane: [Faktury](10_faktury.md) · [Formularz](10b_formularz_faktury.md)
