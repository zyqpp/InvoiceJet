import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";
import { IFirm } from "../models/IFirm";
import { HttpClient } from "@angular/common/http";
import { Subject } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class FirmService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  public addFirm(firm: IFirm, isClient: boolean = true) {
    return this.http.post<IFirm>(
      `${this.baseUrl}/Firm/AddFirm/${isClient}`,
      firm
    );
  }

  public editFirm(firm: IFirm, isClient: boolean = true) {
    return this.http.put<IFirm>(
      `${this.baseUrl}/Firm/EditFirm/${isClient}`,
      firm
    );
  }

  public getUserActiveFirm() {
    return this.http.get<IFirm>(`${this.baseUrl}/Firm/GetUserActiveFirm/`);
  }

  public getUserClientFirms() {
    return this.http.get<IFirm[]>(`${this.baseUrl}/Firm/GetUserClientFirms/`);
  }

  public getFirmFromAnaf(cuiValue: string) {
    return this.http.get<IFirm>(`${this.baseUrl}/Firm/fromAnaf/${cuiValue}`);
  }

  public deleteFirms(firmIds: number[]) {
    return this.http.put(`${this.baseUrl}/Firm/DeleteFirms/`, firmIds);
  }
}
