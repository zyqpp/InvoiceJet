# 02_dto — Data Transfer Objects

Dokumentacja obiektów DTO (Data Transfer Objects) projektu InvoiceJet. DTO stanowią warstwę kontraktu między frontendem (Angular 16) a backendem (ASP.NET Core 8) — definiują kształt danych przesyłanych przez API. Projekt wykorzystuje 14 DTO pogrupowanych według kierunku użycia (żądanie, odpowiedź, dwukierunkowe) i domeny biznesowej.

## Drzewo zawartości

```
02_dto/
├── README.md                                  — ten plik
├── spis_dto.md                                — zbiorczy spis wszystkich 14 DTO z tabelą
├── DTO-01_RegisterUserDto.md                  — DTO rejestracji użytkownika (Request)
├── DTO-02_LoginUserDto.md                     — DTO logowania (Request)
├── DTO-03_FirmRequestDto.md                   — DTO danych firmy (dwukierunkowy)
├── DTO-04_BankAccountRequestDto.md            — DTO konta bankowego (dwukierunkowy)
├── DTO-05_ProductRequestDto.md                — DTO produktu/usługi (dwukierunkowy)
├── DTO-06_DocumentSeriesRequestDto.md         — DTO serii numeracji (dwukierunkowy)
├── DTO-07_DocumentRequestDto.md               — DTO dokumentu głównego (dwukierunkowy)
├── DTO-08_DocumentProductRequestDto.md        — DTO pozycji dokumentu (zagnieżdżony)
├── DTO-09_DocumentTableRecordDto.md           — DTO rekordu listy dokumentów (Response)
├── DTO-10_DocumentAutofillInfoDto.md          — DTO danych autouzupełnienia (Response)
├── DTO-11_DocumentStatusDto.md                — DTO statusu dokumentu (Response/zagnieżdżony)
├── DTO-12_DashboardStatsDto.md                — DTO statystyk dashboardu (Response)
├── DTO-13_UserDto.md                          — DTO tokenu JWT (Response)
└── DTO-14_UserFirmDto.md                      — DTO powiązania User-Firm (Response)
```

## Kluczowe dokumenty

| Dokument | Opis |
|---|---|
| [spis_dto.md](spis_dto.md) | Zbiorczy spis wszystkich 14 DTO z kierunkiem i endpointem |
| [DTO-07_DocumentRequestDto.md](DTO-07_DocumentRequestDto.md) | Najbardziej złożony DTO — agreguje dane dokumentu z zagnieżdżonymi obiektami |
| [DTO-10_DocumentAutofillInfoDto.md](DTO-10_DocumentAutofillInfoDto.md) | Agregat danych formularza — eliminuje wiele wywołań API |

## Konwencje nazewnicze

Pliki nazwane `DTO-XX_NazwaDto.md` gdzie XX to numer porządkowy (01..14). Nazwy DTO cytowane 1:1 z kodu C#.

## Powiązane katalogi

| Katalog | Powiązanie |
|---|---|
| [01_db/](../01_db/) | Encje EF Core — źródło/cel mapowania dla DTO |
| [05_automapper/](../05_automapper/) | Profile AutoMapper realizujące mapowania encja ↔ DTO |
| [04_api_i_integracje/](../../04_api_i_integracje/) | Endpointy API przyjmujące/zwracające te DTO |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — reorganizacja z 03_dto/. |
