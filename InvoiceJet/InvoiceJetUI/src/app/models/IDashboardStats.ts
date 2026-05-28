import { IMonthlyTotal } from "./IMonthlyTotal";

export interface IDashboardStats {
  totalDocuments: number;
  totalClients: number;
  totalProducts: number;
  totalBankAccounts: number;
  monthlyTotals?: IMonthlyTotal[];
}
