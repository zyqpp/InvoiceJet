# Reguły dekompozycji procesów

**Obowiązuje:** Dokumentacja AOS backendu InvoiceJetAPI
**Cel:** Usunąć dwuznaczność „czym jest proces", aby kolejni agenci pracowali jednoznacznie.

---

## 1. Model dwupoziomowy

Dokumentację organizujemy na dwóch poziomach, które się uzupełniają:

| Poziom | Jednostka | Plik(i) | Dla kogo przede wszystkim |
|---|---|---|---|
| Biznesowy | **proces** (`P-XX`) = zdolność biznesowa | katalogi `processes/P-XX_*` | Analityk, Developer |
| Techniczny | **endpoint** (`API-XX`) = jedna metoda HTTP | `KATALOG_API.md` | Tester, Developer |

Każdy endpoint występuje **dokładnie raz** w `KATALOG_API.md` i jest przypisany do dokładnie jednego procesu. Każdy proces wymienia wszystkie swoje endpointy.

---

## 2. Reguła deterministyczna: co jest jednym procesem

Proces grupuje endpointy realizujące **jedną zdolność biznesową na jednym zasobie**, zwykle w jednym kontrolerze. Stosuj reguły w kolejności:

1. **Rodzina CRUD jednego zasobu = jeden proces.** Operacje list/get/add/edit/delete tego samego zasobu (np. produktów) tworzą jeden proces typu „Zarządzanie X". W pliku `02_KONTRAKT_API` każdy endpoint dostaje osobny blok.
2. **Odrębny cel użytkownika = odrębny proces.** Jeśli endpoint realizuje inny cel biznesowy, ma własne warunki wstępne i inny skutek (np. „Wystawienie faktury" vs „Generowanie PDF" vs „Transformacja do storna"), to jest osobny proces — nawet jeśli leży w tym samym kontrolerze.
3. **Operacja read-only wspierająca inny proces** (np. „dane autouzupełniania", „lista + szczegóły") może być osobnym procesem, jeśli ma własny endpoint i własny kontrakt.
4. **Jeden endpoint może należeć tylko do jednego procesu.** W razie wątpliwości przypisuje się go do procesu, którego cel realizuje bezpośrednio.

> Reguła rozstrzygająca: jeżeli wahasz się między „jeden proces z wieloma endpointami" a „kilka procesów", zapytaj „czy analityk nazwałby to jedną funkcją aplikacji?". Jeśli tak — jeden proces.

---

## 3. Numeracja

- Procesy: `P-01`, `P-02`, … w kolejności dokumentowania (numer nie musi odpowiadać kolejności kontrolerów).
- Endpointy w katalogu API: `API-01`, `API-02`, … w kolejności kontroler → metoda.
- Numery są stałe. Wycofany proces zachowuje numer (oznaczony jako wycofany), nie jest nadawany ponownie.

---

## 4. Nazewnictwo katalogu procesu

Format: `P-XX_NazwaWUpperCamelCase`, np. `P-09_ManageProducts`. Nazwa opisuje zdolność biznesową po angielsku (spójnie z nazewnictwem kodu).

---

## 5. Złączenie z frontendem (odłożone)

Most do AOS frontendu (`MAPA_FULLSTACK.md`) jest przygotowany strukturalnie, ale **nie wypełniany** na tym etapie. Gdy ruszy:

- każdy proces zyska pole „Powiązana funkcja frontu",
- klucz złączenia: identyfikator funkcji frontu (schemat ustali AOS frontendu).

Do tego czasu nie wstawiaj zgadywanych powiązań — pozostaw marker `[POZA ZAKRESEM — ETAP FULLSTACK]`.

---

## 6. Mapa procesów do re-dokumentacji (z archiwum)

Stare procesy `P-01`..`P-19` zostały zarchiwizowane w `docs/aos/backend/_archive/processes/` i **nie są źródłem prawdy**. Poniższa mapa odpowiada ich pierwotnemu podziałowi i służy wyłącznie jako **punkt startowy** przy re-dokumentacji wg nowych szablonów (numery i nazwy mogą się zmienić po weryfikacji wobec aktualnego kodu — zasada `ZB.1`).

| Kontroler | Procesy z archiwum (do re-dokumentacji) |
|---|---|
| `AuthController` | rejestracja użytkownika, logowanie użytkownika |
| `FirmController` | dodanie firmy, pobranie firmy z ANAF, edycja firmy, pobranie aktywnej firmy użytkownika, firmy-klienci |
| `ProductController` | zarządzanie produktami (CRUD) |
| `BankAccountController` | zarządzanie kontami bankowymi (CRUD) |
| `DocumentSeriesController` | zarządzanie seriami dokumentów (CRUD) |
| `DocumentController` | wystawienie faktury, dane autouzupełniania, edycja dokumentu, lista i szczegóły dokumentów, usuwanie dokumentów, generowanie PDF, strumień PDF faktury, statystyki dashboardu, transformacja do storna |

Numery `P-XX` w nowej dokumentacji zostaną nadane w kolejności dokumentowania — niekoniecznie zgodnie z archiwum.
