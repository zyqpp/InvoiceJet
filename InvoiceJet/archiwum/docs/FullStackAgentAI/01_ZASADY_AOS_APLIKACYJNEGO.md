# Zasady AOS aplikacyjnego

**Obowiazuje:** dokumentacja end-to-end w `docs/aos/application`

## 1. Cel dokumentacji

AOS aplikacyjny opisuje działanie InvoiceJet przez połączenie trzech warstw:

- makieta i komponent Angular,
- serwis HTTP i endpoint API,
- serwis backendowy, encja, tabela i kolumna bazy danych.

Dokument nie zastępuje AOS frontendu ani AOS backendu. Dokument wskazuje ich powiązania i pokazuje pełny ślad danych oraz operacji.

## 2. Źródła prawdy

| Obszar | Źródło |
|---|---|
| Menu, trasy i makiety | `InvoiceJet/InvoiceJetUI/docs` |
| Modele, serwisy i operacje frontendu | `InvoiceJet/InvoiceJetUI/docs/aos/frontend` |
| Endpointy i procesy backendu | `InvoiceJet/InvoiceJetAPI/docs/aos/backend` |
| Reguły dla agentow front/back | `InvoiceJet/InvoiceJetUI/docs/FrontendAgentAI`, `InvoiceJet/InvoiceJetAPI/docs/BackendAgentAI` |
| Technologia i baza | `docs/stos-technologiczny.md` |
| Struktura frontendu | `docs/struktura-katalogow-frontend.md` |

## 3. Reguły nadrzedne

| Kod | Reguła | Opis |
|---|---|---|
| ZA.1 | Dokumentacja źródłowa jest podstawa | Opis musi wynikac z dokumentacji frontendu, backendu albo dokumentów głównych. |
| ZA.2 | Pełny ślad danych | Każde pole danych łączy UI, API, DTO, encje i bazę, jeżeli taki ślad istnieje. |
| ZA.3 | Brak zgadywania SQL | Przy EF Core opisuje się metodę, encje, tabele i kolumny na podstawie dokumentacji backendu. |
| ZA.4 | Dokument nie powiela całych AOS | Dokument aplikacyjny streszcza powiązanie i linkuje do dokumentów źródłowych. |
| ZA.5 | Tylko informacje użyteczne | Nie dodawac opisow, ktore nie pomagaja analitykowi, developerowi albo testerowi. |

## 4. Styl

Opis biznesowy jest po polsku. Nazwy klas, metod, endpointów, pól DTO, kolumn i plików zachowują oryginalne brzmienie i są zapisywane w backtickach.

Zdania są krotkie. Jedno zdanie opisuje jedna decyzje, jedna zaleznosc albo jeden skutek.

Agent nie czyta kodu aplikacji podczas twórzenia AOS aplikacyjnego. Jeżeli dokumentacja frontendu albo backendu wskazuje nazwe pliku, klasy lub metody, agent moze ja przytoczyc jako ślad z dokumentacji.

## 5. Zakres przepływu

Przepływ aplikacyjny zaczyna sie w elemencie widocznym dla użytkownika. Przepływ kończy sie na skutku:

- zmianie danych w bazie,
- odczycie danych z bazy,
- wygenerowaniu pliku,
- zmianie stanu widoku,
- komunikacie sukcesu albo błędu.
