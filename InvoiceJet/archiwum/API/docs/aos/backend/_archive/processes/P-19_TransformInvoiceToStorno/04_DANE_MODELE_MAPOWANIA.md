# Transformacja faktury do storna — Dane, modele i mapowania

## Wejście

| Element | Typ | Rola |
|---|---|---|
| `documentIds` | `int[]` | Identyfikatory dokumentów do transformacji. |

---

## Encje

| Encja | Pole modyfikowane |
|---|---|
| `Document` | `DocumentTypeId` |

---

## Enum

| Enum | Wartość |
|---|---|
| `DocumentTypeEnum.StornoInvoice` | `3` |
