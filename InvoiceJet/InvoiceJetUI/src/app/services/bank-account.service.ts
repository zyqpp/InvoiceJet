import { Injectable } from "@angular/core";
import { IBankAccount } from "../models/IBankAccount";
import { HttpClient } from "@angular/common/http";
import { environment } from "src/environments/environment";

@Injectable({
  providedIn: "root",
})
export class BankAccountService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getUserFirmBankAccounts() {
    return this.http.get<IBankAccount[]>(
      `${this.baseUrl}/BankAccount/GetUserFirmBankAccounts/`
    );
  }

  addBankAccount(bankAccount: IBankAccount) {
    return this.http.post<IBankAccount>(
      `${this.baseUrl}/BankAccount/AddUserFirmBankAccount/`,
      bankAccount
    );
  }

  editBankAccount(bankAccount: IBankAccount) {
    return this.http.put<IBankAccount>(
      `${this.baseUrl}/BankAccount/EditUserFirmBankAccount/`,
      bankAccount
    );
  }

  deleteBankAccounts(bankAccountIds: number[]) {
    return this.http.put<number[]>(
      `${this.baseUrl}/BankAccount/DeleteUserFirmBankAccounts`,
      bankAccountIds
    );
  }
}
