import { HttpClient } from "@angular/common/http";
import { Injectable } from '@angular/core';
import { environment } from "src/environments/environment";
import { IRegisterUser } from "../models/IRegisterUser";

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient) { }

  private baseUrl = environment.apiUrl;

  public getUserByEmail(email: string) {
    return this.http.get<IRegisterUser>(
      this.baseUrl + '/User/GetUserByEmail/' + email,
    );
  }
}
