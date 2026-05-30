# Edycja firmy — Logika aplikacyjna

## Przepływ wykonania

1. Kontroler wywołuje `FirmService.EditFirm(firmDto, isClient)`.
2. Serwis pobiera encję firmy przez `Firms.GetByIdAsync(firmDto.Id)`.
3. Gdy encja nie istnieje, serwis rzuca `Exception("Firm not found.")`.
4. Serwis mapuje `firmDto` na istniejącą encję przez `_mapper.Map(firmDto, firm)`.
5. Serwis wykonuje `_unitOfWork.CompleteAsync()`.
6. Serwis wywołuje `ManageUserFirmRelation(firm.Id, isClient)`.
7. `ManageUserFirmRelation` aktualizuje lub tworzy relację `UserFirm` i wykonuje `CompleteAsync()`.
8. Serwis zwraca `firmDto`, a kontroler zwraca `200 OK`.

---

## Uwagi

- Metoda nie weryfikuje własności firmy względem użytkownika przed aktualizacją encji `Firm`. [UWAGA: sprawdzenie uprawnień do konkretnego rekordu `Firm` nie jest widoczne w kodzie procesu — WYMAGA WERYFIKACJI Z ZESPOŁEM]
