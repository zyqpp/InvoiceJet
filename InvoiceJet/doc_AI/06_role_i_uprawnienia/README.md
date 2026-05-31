# 06_role_i_uprawnienia — Role i uprawnienia

Opis biznesowy: [do uzupełnienia w fazie 11]

## Drzewo zawartości

```
06_role_i_uprawnienia/
├── README.md
├── lista_rol.md                     ← tabela wszystkich ról (1 rola: User)
├── lista_uprawnien.md               ← uprawnienia (JWT, [Authorize(Roles = "User")])
├── macierz_role_uprawnienia.md      ← macierz: rola × uprawnienie × endpointy
└── User.md                          ← opis roli User
```

## Kluczowe dokumenty

- [`macierz_role_uprawnienia.md`](macierz_role_uprawnienia.md)

## Uwagi

Aplikacja ma jedną rolę: `User`. Wszystkie chronione endpointy wymagają atrybutu `[Authorize(Roles = "User")]`. Endpointy publiczne: `POST /api/Auth/register`, `POST /api/Auth/login`.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet. |
