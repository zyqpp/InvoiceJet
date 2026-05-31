# Jak wygląda wydrukowany dokument PDF

![Podgląd dokumentu PDF](../assets/screens/pdf_podglad.png)

## Co to jest?

Ten dokument opisuje **co pojawi się na wydruku (PDF)** faktury, proformy lub storna.
Pokazuje które pola z formularza trafiają na dokument, co jest wyliczane automatycznie, a co pochodzi z ustawień firmy.

---

## Układ dokumentu — 4 sekcje

```
┌────────────────────────────────────────────────────┐
│  NAGŁÓWEK                                          │
│  Numer dokumentu · Daty · Znacznik statusu         │
├────────────────────────────────────────────────────┤
│  ADRESY                                            │
│  Od (Twoja firma + konto bankowe) │ Dla (klient)   │
├────────────────────────────────────────────────────┤
│  TABELA POZYCJI                                    │
│  Lp · Produkt · Ilość · Cena · Wartość · VAT       │
│  ─────────────────────────────────────────────     │
│  Podsumowanie: Wartość netto · VAT · Do zapłaty    │
├────────────────────────────────────────────────────┤
│  STOPKA: Strona X / Y                              │
└────────────────────────────────────────────────────┘
```

---

## Sekcja 1: Nagłówek

| Pole na PDF | Co to jest | Skąd pochodzi |
|---|---|---|
| **Numer dokumentu** | np. `Invoice #FV0005` | Seria + numer z formularza → wygenerowany automatycznie |
| **Issue date** | Data wystawienia | Pole **Issue Date** z [formularza](10b_formularz_faktury.md) |
| **Due date** | Termin płatności | Pole **Due Date** z [formularza](10b_formularz_faktury.md) (jeśli podane) |
| **Znacznik statusu** | kolorowy prostokąt | Patrz tabela poniżej |

### Znacznik statusu (badge) — różni się dla każdego typu

| Typ dokumentu | Kolor | Tekst |
|---|---|---|
| Faktura — nieopłacona | 🔴 Czerwony | „Unpaid" |
| Faktura — opłacona | 🟢 Zielony | „Paid" |
| Proforma | 🟡 Żółty | „Proforma" |
| Storno (korekta) | 🟡 Żółty | „Storno" |

Status faktury zmieniasz w polu **Status** w [formularzu](10b_formularz_faktury.md).

---

## Sekcja 2: Blok „Od" (Twoja firma)

Ten blok aplikacja wypełnia **automatycznie** na podstawie:
- Twoich danych firmy z ustawień → [Dane firmy](05_dane_firmy.md)
- Twojego konta bankowego → [Konta bankowe](07_konta_bankowe.md)

**Nie musisz tego wpisywać w formularzu faktury.**

| Pole na PDF | Skąd pochodzi |
|---|---|
| Nazwa firmy | [Dane firmy](05_dane_firmy.md) → pole **Firm Name** |
| Adres | [Dane firmy](05_dane_firmy.md) → pole **Address** |
| Miasto, okręg | [Dane firmy](05_dane_firmy.md) → pola **City**, **County** |
| CUI | [Dane firmy](05_dane_firmy.md) → pole **CUI** (jeśli wypełnione) |
| Reg. Com | [Dane firmy](05_dane_firmy.md) → pole **Reg. Com.** (jeśli wypełnione) |
| Nazwa banku | [Konta bankowe](07_konta_bankowe.md) → pole **Bank Name** |
| IBAN | [Konta bankowe](07_konta_bankowe.md) → pole **IBAN** |

> ⚠️ **Ważne:** aplikacja automatycznie wybiera **pierwsze** konto bankowe przypisane do Twojej firmy. Jeśli masz kilka kont, na PDF trafi to, które zostało dodane jako pierwsze.

---

## Sekcja 2: Blok „Dla" (klient)

| Pole na PDF | Skąd pochodzi |
|---|---|
| Nazwa firmy | Pole **Client** w [formularzu faktury](10b_formularz_faktury.md) → z bazy [Klientów](06_klienci.md) |
| Adres | Dane klienta z bazy [Klientów](06_klienci.md) |
| Miasto, okręg | Dane klienta z bazy [Klientów](06_klienci.md) |
| CUI | Dane klienta z bazy [Klientów](06_klienci.md) (jeśli wypełnione) |
| Reg. Com | Dane klienta z bazy [Klientów](06_klienci.md) (jeśli wypełnione) |
| Konto bankowe klienta | ❌ **Nie pojawia się** — blok „Dla" nie zawiera konta bankowego |

---

## Sekcja 3: Tabela pozycji

### Kolumny tabeli

| Kolumna PDF | Co pokazuje | Skąd pochodzi | Wyliczane? |
|---|---|---|---|
| **#** | Numer porządkowy (1, 2, 3…) | automatycznie | ✅ TAK |
| **Product** | Nazwa produktu/usługi | Kolumna **Name** w pozycji | ❌ NIE — wprost z formularza |
| **Qt.** | Ilość | Kolumna **Quantity** w pozycji | ❌ NIE — wprost z formularza |
| **Unit price** | Cena jednostkowa netto | Kolumna **Unit Price** w pozycji | ❌ NIE — wprost z formularza |
| **Value** | Wartość netto wiersza | Unit price × Quantity | ✅ **TAK** — wyliczane |
| **Total TVA** | Kwota podatku VAT w wierszu | Total cena brutto − (Unit price × Qty) | ✅ **TAK** — wyliczane |

### Jak są wyliczane pozycje

```
Wartość netto wiersza (Value)   = Unit Price × Quantity
Kwota VAT wiersza (Total TVA)   = Cena brutto pozycji − (Unit Price × Quantity)
```

> **Cena brutto pozycji** = to co wpisujesz w polu **Unit Price**, przemnożone przez ilość i powiększone o VAT zgodnie z polem **TVA Value**. Jest wyliczana i zapisywana w momencie wystawienia.

### Ważne: ceny są zapamiętane na stałe

Ceny na PDF odpowiadają **wartościom z momentu wystawienia dokumentu**. Jeśli później zmienisz cenę produktu w [katalogu produktów](08_produkty.md), starsze faktury **nie zmienią się** — wydruk zostaje taki jaki był.

---

## Sekcja 3: Podsumowanie (pod tabelą)

| Wiersz | Co pokazuje | Formuła |
|---|---|---|
| **Subtotal** | Suma wartości netto wszystkich pozycji | Σ (Unit Price × Quantity) |
| *(obok Subtotal)* | Suma VAT wszystkich pozycji | Σ (Cena brutto − Unit Price × Qty) |
| **Total pay** | Łączna kwota do zapłaty | Subtotal + łączny VAT |

Kwota **Total pay** wyświetlana jest pogrubioną czcionką i zakończona „lei".

---

## Faktury korygujące (storno) — wartości ujemne

Na stornach wszystkie kwoty wyświetlane są jako **ujemne** (ze znakiem minus):
- Ilości: `-Qt.`
- Ceny: `-Unit price`
- Wartości: `-Value`, `-Total TVA`
- Podsumowanie: `-Subtotal`, `-Total pay`

To standardowe oznaczenie korekty — pokazuje że cofasz wcześniejszą transakcję.

---

## Sekcja 4: Stopka strony

Stopka na dole każdej strony zawiera numer strony w formacie `X / Y` (np. `1 / 2`). Pojawia się automatycznie na każdej stronie, jeśli dokument ma więcej niż jedną.

---

## Co MUSISZ wypełnić przed wygenerowaniem PDF

| Wymagane | Gdzie to ustawić |
|---|---|
| Dane swojej firmy | [Dane firmy](05_dane_firmy.md) (wystarczy raz) |
| Konto bankowe firmy | [Konta bankowe](07_konta_bankowe.md) (wystarczy raz) |
| Klient | [Klienci](06_klienci.md) → pole Client w formularzu |
| Data wystawienia | Formularz → Issue Date |
| Pozycje (produkty) | Formularz → tabela pozycji |

---

## Jak wygenerować PDF → [P-10 Generowanie PDF](../02_procesy/P-10_generowanie_pdf.md)

---

🔗 Powiązane: [Formularz faktury](10b_formularz_faktury.md) · [Dane firmy](05_dane_firmy.md) · [Konta bankowe](07_konta_bankowe.md) · [Klienci](06_klienci.md) · [Faktury](10_faktury.md) · [Proformy](11_proformy.md) · [Storna](12_storna.md)
