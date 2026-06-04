# A-00: AppShell — Walidacje, Błędy, Bezpieczeństwo

## A. Walidacje

AppShell nie zawiera formularzy ani pól tekstowych wymagających walidacji. Walidacje formularzy znajdują się w:
- **A-11: Login** — walidacja emailu i hasła
- **A-12: Register** — walidacja emailu, hasła, potwierdzenia hasła

### Walidacja w AppShell

| Element | Typ | Frontend Validator | Backend Validator | Efekt |
|---|---|---|---|---|
| Pole Search (sidebar) | Input | Brak (przyjmuje dowolny tekst) | N/D | Tekstowe filtrowanie in-memory |
| Token JWT | N/D | AuthService.isLoggedIn() sprawdza czy token istnieje w localStorage | Weryfikacja tokenu na backendzie (AuthInterceptor) | Brak tokenu → AuthGuard blokuje dostęp |
| Dark Mode toggle | N/D | Brak (toggle logiki, nie validacji) | N/D | Zmiana klasy CSS |

## B. Guardy — Kontrola dostępu do tras

### AuthGuard

**Cel:** Blokowanie dostępu do tras chronionych bez tokenu JWT

**Implementacja:**

```typescript
// app.guard.ts
@Injectable()
export class AuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (this.authService.isLoggedIn()) {
      return true;
    } else {
      this.router.navigate(['/login']);
      return false;
    }
  }
}
```

**Gdzie jest użyty:**
- Wszystkie trasy oprócz `/login` i `/register` mają `canActivate: [AuthGuard]`

**Co się dzieje:**
- Jeśli token istnieje → dostęp do trasy
- Jeśli token brakuje lub wygasł → redirect na `/login`

**Status HTTP:** N/D — guard pracuje na poziomie klienta (localStorage)

---

## C. Interceptory HTTP — Obsługa tokenu i błędów

### AuthInterceptor

**Cel:** Dodawanie tokenu JWT do każdego żądania HTTP, obsługa błędu 401 (token wygasł)

**Implementacja:**

```typescript
// auth.interceptor.ts
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('authToken');
    if (token) {
      req = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    return next.handle(req).pipe(
      catchError(error => {
        if (error.status === 401) {
          this.authService.logout();
          // Redirect na /login przez LogoutService
        }
        throw error;
      })
    );
  }
}
```

**Gdzie jest użyty:**
- Globalnie dla wszystkich żądań HTTP (providedIn: 'root')

**Co się dzieje:**
1. Każde żądanie HTTP ma nagłówek `Authorization: Bearer {token}`
2. Jeśli serwer zwróci 401 (Unauthorized), token jest usuwany z localStorage
3. Użytkownik zostaje wylogowany i przekierowany na `/login`

**Status HTTP:** 401 → token wygasł

---

### ErrorInterceptor

**Cel:** Centralna obsługa błędów HTTP i wyświetlanie ich użytkownikowi

**Implementacja:**

```typescript
// error.interceptor.ts
@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private toastr: ToastrService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError(error => {
        let errorMessage = 'An error occurred';
        
        if (error.error instanceof ErrorEvent) {
          // Client-side error
          errorMessage = error.error.message;
        } else {
          // Server-side error
          errorMessage = `Error: ${error.status} - ${error.statusText}`;
        }

        this.toastr.error(errorMessage);
        throw error;
      })
    );
  }
}
```

**Gdzie jest użyty:**
- Globalnie dla wszystkich żądań HTTP (providedIn: 'root')

**Co się dzieje:**
- Każdy błąd HTTP (400, 401, 404, 500) jest wyświetlony w toastrze (powiadomienie)
- Błędy klienta (network errors) też są obsługiwane

**Obsługiwane kody HTTP:**
- **400 Bad Request** → "Error: 400 - Bad Request"
- **401 Unauthorized** → Obsłużony przez AuthInterceptor (logout)
- **404 Not Found** → "Error: 404 - Not Found"
- **500 Internal Server Error** → "Error: 500 - Internal Server Error"

---

## D. Bezpieczeństwo — Autoryzacja

### Token JWT

**Przechowywanie:**
- `localStorage.setItem('authToken', token)` — token otrzymywany z backendu po logowaniu (A-11: Login)

**Użycie:**
- AuthService: `AuthService.isLoggedIn()` sprawdza czy token istnieje
- AuthInterceptor: dodaje token do nagłówka HTTP
- NavbarComponent: dekoduje token, wyciąga imię i email

**Bezpieczeństwo:**
- Token wysyłany tylko w nagłówku `Authorization: Bearer ...`
- Token NIE jest wysyłany w cookie (ochrona przed CSRF)
- [WYMAGA WERYFIKACJI] Token nie jest weryfikowany na kliencie — tylko pobierany i dekodowany

**Wygaśnięcie:**
- Jeśli backend zwróci 401, token jest usuwany z localStorage
- [WYMAGA WERYFIKACJI] Czy backend wysyła refresh token do odnawiania sesji?

### Dane w localStorage

| Klucz | Wartość | Bezpieczeństwo |
|---|---|---|
| `authToken` | JWT token | localStorage jest dostępny dla wszystkich skryptów na tej domenie (XSS risk) |

**[UWAGA] Potencjalne zagrożenie XSS:** Jeśli aplikacja ma lukę XSS, atakujący może ukraść token z localStorage. Rozwiązanie: stosować HttpOnly cookies (ale to wymaga zmian na backendzie).

---

## E. Błędy i obsługa

| Błąd | Warstwa | Gdzie | Komunikat | Reaction |
|---|---|---|---|---|
| Brak tokenu | Frontend (Guard) | AuthGuard | Brak (cichy redirect) | Redirect na `/login` |
| Token wygasł | Frontend (Interceptor) | AuthInterceptor | "Error: 401 - Unauthorized" (z ErrorInterceptor) | Logout, redirect na `/login` |
| Błąd 400 Bad Request | Frontend (Interceptor) | ErrorInterceptor | "Error: 400 - Bad Request" | Toast error (toastr.error) |
| Błąd 404 Not Found | Frontend (Interceptor) | ErrorInterceptor | "Error: 404 - Not Found" | Toast error |
| Błąd 500 Server Error | Frontend (Interceptor) | ErrorInterceptor | "Error: 500 - Internal Server Error" | Toast error |
| Network error | Frontend (Interceptor) | ErrorInterceptor | Error message z ErrorEvent | Toast error |

---

## F. Kontrola dostępu — Tabela uprawnień

| Trasa | Chroniona | Guard | Widoczne dla |
|---|---|---|---|
| `/login` | ✗ Publiczna | — | Niezalogowani |
| `/register` | ✗ Publiczna | — | Niezalogowani |
| `/dashboard` | ✓ Chroniona | AuthGuard | Zalogowani |
| `/documents/*` | ✓ Chroniona | AuthGuard | Zalogowani |
| `/inventory/*` | ✓ Chroniona | AuthGuard | Zalogowani |
| `/settings/*` | ✓ Chroniona | AuthGuard | Zalogowani |

**[WYMAGA WERYFIKACJI]** Czy istnieją role (admin, user)? Czy tylko bycie zalogowanym jest wystarczające?

---

## G. Dane wrażliwe

| Dane | Gdzie | Bezpieczeństwo | Status |
|---|---|---|---|
| Token JWT | localStorage | Dostępny dla XSS | [WYMAGA WERYFIKACJI] czy token zawiera dane wrażliwe? |
| Hasło | N/D (nie w AppShell) | Wysyłane tylko w POST do backendu (A-11) | [WYMAGA WERYFIKACJI] czy hasło jest hashowane na backendzie |
| Email użytkownika | Wyświetlany w navbar | Pobierany z tokenu JWT | OK — email jest publiczny |
| Imię użytkownika | Wyświetlany w navbar | Pobierany z tokenu JWT | OK — imię jest publiczne |

---

## H. Podsumowanie zabezpieczeń

✓ **Co jest zabezpieczone:**
- Trasy chronione mają AuthGuard
- Token JWT dodawany do każdego żądania
- Błędy HTTP są obsługiwane centralnie
- Token usuwany z localStorage przy wygaśnięciu (401)

⚠️ **Co wymaga weryfikacji:**
- Czy token nie zawiera haseł ani danych wrażliwych?
- Czy jest implementowany refresh token?
- Czy istnieje ochrona przed CSRF (Cross-Site Request Forgery)?
- Czy aplikacja jest chroniona przed XSS (Cross-Site Scripting)?
- Czy role użytkownika są sprawdzane na backendzie?

❌ **Potencjalne luki:**
- localStorage jest podatne na XSS (powinny być HttpOnly cookies)
- Dane użytkownika są dekodowane z tokenu bez weryfikacji na backendzie
- Tryb ciemny nie jest utrwalany (mniej istotne, ale UX)
