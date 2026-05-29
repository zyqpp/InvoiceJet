# Pobranie aktywnej firmy użytkownika — Logika aplikacyjna

## Przepływ wykonania

1. Kontroler wywołuje `FirmService.GetUserActiveFirm()`.
2. Serwis pobiera relację aktywnej firmy użytkownika przez:
   - `_userService.GetCurrentUserId()`,
   - `_unitOfWork.Users.GetUserFirmAsync(userId)`.
3. Gdy relacja nie istnieje, serwis zwraca `new FirmDto()`.
4. Gdy relacja istnieje, serwis mapuje `activeUserFirm.Firm` do `FirmDto`.
5. Kontroler zwraca `200 OK`.
