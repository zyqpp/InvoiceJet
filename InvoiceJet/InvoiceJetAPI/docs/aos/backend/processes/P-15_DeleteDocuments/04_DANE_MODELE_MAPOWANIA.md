# Usuwanie dokumentów — Dane, modele i mapowania

## Dane wejściowe

| Element | Typ | Rola |
|---|---|---|
| `documentIds` | `int[]` | Lista identyfikatorów dokumentów do usunięcia. |

---

## Encje

| Encja | Rola |
|---|---|
| `Document` | Rekord główny usuwany w procesie. |
| `DocumentProduct` | Rekordy zależne usuwane przed usunięciem dokumentu. |
