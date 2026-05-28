import { Currency } from "../enums/Currency";

export interface IBankAccount {
  id?: number;
  bankName: string;
  iban: string;
  currency: Currency;
  isActive: boolean;
}
