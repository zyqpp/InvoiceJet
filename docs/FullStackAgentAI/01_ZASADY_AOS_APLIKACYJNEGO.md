# Zasady AOS aplikacyjnego

**Obowiazuje:** dokumentacja end-to-end w `docs/aos/application`

## 1. Cel dokumentacji

AOS aplikacyjny opisuje dzialanie InvoiceJet przez polaczenie trzech warstw:

- makieta i komponent Angular,
- serwis HTTP i endpoint API,
- serwis backendowy, encja, tabela i kolumna bazy danych.

Dokument nie zastepuje AOS frontendu ani AOS backendu. Dokument wskazuje ich powiazania i pokazuje pelny slad danych oraz operacji.

## 2. Zrodla prawdy

| Obszar | Zrodlo |
|---|---|
| Menu, trasy i makiety | `InvoiceJet/InvoiceJetUI/docs` |
| Modele, serwisy i operacje frontendu | `InvoiceJet/InvoiceJetUI/docs/aos/frontend` |
| Endpointy i procesy backendu | `InvoiceJet/InvoiceJetAPI/docs/aos/backend` |
| Reguly dla agentow front/back | `InvoiceJet/InvoiceJetUI/docs/FrontendAgentAI`, `InvoiceJet/InvoiceJetAPI/docs/BackendAgentAI` |
| Technologia i baza | `docs/stos-technologiczny.md` |
| Struktura frontendu | `docs/struktura-katalogow-frontend.md` |

## 3. Reguly nadrzedne

| Kod | Regula | Opis |
|---|---|---|
| ZA.1 | Dokumentacja zrodlowa jest podstawa | Opis musi wynikac z dokumentacji frontendu, backendu albo dokumentow glownych. |
| ZA.2 | Pelny slad danych | Kazde pole danych laczy UI, API, DTO, encje i baze, jezeli taki slad istnieje. |
| ZA.3 | Brak zgadywania SQL | Przy EF Core opisuje sie metode, encje, tabele i kolumny na podstawie dokumentacji backendu. |
| ZA.4 | Dokument nie powiela calych AOS | Dokument aplikacyjny streszcza powiazanie i linkuje do dokumentow zrodlowych. |
| ZA.5 | Tylko informacje uzyteczne | Nie dodawac opisow, ktore nie pomagaja analitykowi, developerowi albo testerowi. |

## 4. Styl

Opis biznesowy jest po polsku. Nazwy klas, metod, endpointow, pol DTO, kolumn i plikow zachowuja oryginalne brzmienie i sa zapisywane w backtickach.

Zdania sa krotkie. Jedno zdanie opisuje jedna decyzje, jedna zaleznosc albo jeden skutek.

Agent nie czyta kodu aplikacji podczas tworzenia AOS aplikacyjnego. Jezeli dokumentacja frontendu albo backendu wskazuje nazwe pliku, klasy lub metody, agent moze ja przytoczyc jako slad z dokumentacji.

## 5. Zakres przeplywu

Przeplyw aplikacyjny zaczyna sie w elemencie widocznym dla uzytkownika. Przeplyw konczy sie na skutku:

- zmianie danych w bazie,
- odczycie danych z bazy,
- wygenerowaniu pliku,
- zmianie stanu widoku,
- komunikacie sukcesu albo bledu.
