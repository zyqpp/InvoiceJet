# Public - Diagram sekcji

## 1. Diagram

```mermaid
flowchart TD
  Navbar["Navbar public"] --> Login["/login"]
  Navbar --> Register["/register"]
  Login --> LoginApi["POST /api/Auth/login"]
  Register --> RegisterApi["POST /api/Auth/register"]
  LoginApi --> Dashboard["/dashboard"]
  RegisterApi --> Dashboard
```

## 2. Linki

| Pozycja | Route | Dokument pozycji |
|---|---|---|
| Login | `/login` | [Login](./Login/01_MAPA_MAKIET_POZYCJI.md) |
| Register | `/register` | [Register](./Register/01_MAPA_MAKIET_POZYCJI.md) |
