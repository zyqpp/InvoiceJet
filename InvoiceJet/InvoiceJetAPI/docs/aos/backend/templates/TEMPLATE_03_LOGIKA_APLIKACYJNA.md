<!--
SZABLON 03 — LOGIKA APLIKACYJNA (KRĘGOSŁUP: wymiar algorytmu)
Odbiorca priorytetowy: DEVELOPER. To jest najważniejszy plik. Opisz, CO SIĘ DZIEJE PO WYWOŁANIU,
krok po kroku, w kolejności z kodu: WALIDACJE → LOGIKA BIZNESOWA → ZAPISY DO BAZY → ODPOWIEDŹ.
Każdy istotny krok MA cytat kodu i kotwicę `Plik.cs › Klasa.Metoda` (zasady ZB.6, ZB.7).
Definicja ukończenia: 03_MARKERY_I_WERYFIKACJA.md → sekcja 3.
-->

# [NAZWA PROCESU] — Logika aplikacyjna

## 0. Algorytm w skrócie
<!-- Numerowana lista 5–12 kroków całego przepływu. To "spis treści" algorytmu. -->

1. [Kontroler odbiera żądanie i wywołuje serwis.]
2. [Walidacja: ...]
3. [Logika: ...]
4. [Zapis: ...]
5. [Zwrot odpowiedzi.]

---

## 1. Wejście do procesu
<!-- Metoda kontrolera: co odbiera, co wywołuje, co zwraca. Cytat kodu. -->

Kotwica: `[Controller].cs › [Controller].[Method]`

```csharp
// fragment metody kontrolera
```

## 2. Walidacje (faza wejściowa)
<!-- Wymień walidacje W KOLEJNOŚCI sprawdzania. Szczegóły reguł i statusy są w pliku 05; tu pokaż MIEJSCE i KOLEJNOŚĆ w algorytmie. -->

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | [warunek] | `[Service].[Method]` | `[Exception]` (szczegóły: plik 05, `WAL-01`) |

```csharp
// fragment walidacji
```

## 3. Logika biznesowa
<!-- Główne kroki przetwarzania: pobrania danych, obliczenia, budowa encji. Cytaty kodu. -->

[Opis kroku.] Kotwica: `[Service].cs › [...]`

```csharp
// fragment logiki
```

### Tabela: pole encji → źródło
<!-- Dla każdej tworzonej/aktualizowanej encji: skąd bierze się wartość każdego istotnego pola. -->

| Pole encji `[Entity]` | Źródło |
|---|---|
| `[Field]` | `[dto.Field / stała / wynik zapytania]` |

## 4. Zapisy do bazy i transakcje
<!-- Każde wywołanie AddAsync/Update/Remove i KAŻDE CompleteAsync(). Wyjaśnij granice transakcji. -->

| Krok | Operacja | Klasa/metoda | Kiedy `CompleteAsync()` |
|---|---|---|---|
| 1 | [Add/Update/Remove] | `[Repository].[Method]` | [tak/nie — który zapis] |

> Uwaga o transakcyjności: [czy proces ma jawną transakcję obejmującą wszystkie zapisy? Jeśli nie — marker.]

## 5. Odpowiedź
<!-- Co dokładnie zwraca kontroler (obiekt, status, plik). Czy odpowiedź zawiera dane utworzone? -->

[Opis zwracanej odpowiedzi.]

## 6. Uwagi techniczne
<!-- Nieoczywistości algorytmu (np. wyszukiwanie po Name zamiast Id, podwójny zapis, brak transakcji). KAŻDA z markerem. -->

- [Uwaga z markerem lub: „Brak uwag."]

---
<!-- ===== PRZYKŁAD (P-01, fragment) — usuń przed oddaniem =====
2. Walidacja: pobranie aktywnej firmy; brak → UserHasNoAssociatedFirmException.
   Kotwica: DocumentService.cs › DocumentService.AddDocument
   ```csharp
   var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
   if (userFirmId is null) throw new UserHasNoAssociatedFirmException();
   ```
Pole encji Document → źródło: DocumentStatusId | (int)DocumentStatusEnum.Unpaid (stała).
Zapisy: AddAsync(document) + CompleteAsync() (nadaje Id), potem UpdateDocumentProducts + drugie CompleteAsync().
Uwaga: dwa CompleteAsync() bez jawnej transakcji. [UWAGA: ... — WYMAGA WERYFIKACJI Z ZESPOŁEM]
===== KONIEC PRZYKŁADU ===== -->
