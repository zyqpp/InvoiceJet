# Zarządzanie kontami bankowymi — Logika aplikacyjna

## Pobranie listy

1. Serwis wywołuje `BankAccounts.GetUserFirmBankAccountsAsync(currentUserId)`.
2. Dla pustego wyniku zwraca `new List<BankAccountDto>()`.
3. Dla niepustego wyniku mapuje listę do `BankAccountDto`.

## Dodanie konta

1. Serwis mapuje `BankAccountDto` na `BankAccount`.
2. Serwis pobiera `userFirmId` przez `Users.GetUserFirmIdAsync(...)`.
3. Gdy brak aktywnej firmy, rzuca `UserHasNoAssociatedFirmException`.
4. Serwis ustawia `bankAccount.UserFirmId`.
5. Gdy `bankAccount.IsActive == true`, serwis wywołuje `DeactivateOtherBankAccounts(userFirmId)`.
6. Serwis dodaje konto i wykonuje `CompleteAsync()`.

## Edycja konta

1. Serwis pobiera konto po `Id`.
2. Gdy konto nie istnieje, rzuca `Exception("Bank account not found.")`.
3. Serwis mapuje dane wejściowe na encję.
4. Gdy konto jest aktywne, serwis wywołuje `DeactivateOtherBankAccounts(userFirmId, currentAccountId)`.
5. Serwis wykonuje `CompleteAsync()`.

## Usuwanie kont

1. Serwis iteruje po `bankAccountIds`.
2. Dla każdego konta sprawdza, czy istnieje dokument z `Document.BankAccountId == bankAccountId`.
3. Gdy powiązanie istnieje, rzuca `BankAccountAssociatedWithDocumentsException`.
4. Gdy brak powiązania, usuwa konto.
5. Po pętli wykonuje `CompleteAsync()`.
