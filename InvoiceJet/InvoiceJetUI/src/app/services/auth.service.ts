import { UserService } from "./user.service";
import { environment } from "../../environments/environment";
import { Injectable } from "@angular/core";
import { IRegisterUser } from "../models/IRegisterUser";
import { Observable } from "rxjs";
import { ILoginUser } from "../models/ILoginUser";
import { HttpClient, HttpEvent } from "@angular/common/http";
import { JwtHelperService } from "@auth0/angular-jwt";
import { MatDialog } from "@angular/material/dialog";

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private baseUrl = environment.apiUrl;
  private options: any = {
    observe: "response",
    responseType: "text",
  };

  constructor(
    private http: HttpClient,
    private jwtHelper: JwtHelperService,
    public userService: UserService,
    private dialog: MatDialog
  ) {}

  public register(user: IRegisterUser): Observable<{ token: string }> {
    return this.http.post<{ token: string }>(
      this.baseUrl + "/Auth/register",
      user
    );
  }

  public login(user: ILoginUser): Observable<{ token: string }> {
    return this.http.post<{ token: string }>(
      `${this.baseUrl}/Auth/login`,
      user
    );
  }

  public logout(): void {
    localStorage.removeItem("authToken");
  }

  public isLoggedIn(): boolean {
    const token = this.authToken;
    return !!token && !this.jwtHelper.isTokenExpired(token);
  }

  get authToken(): string | null {
    return localStorage.getItem("authToken");
  }

  get decodedToken(): any {
    return this.jwtHelper.decodeToken(this.authToken!);
  }

  get userId(): string {
    return this.decodedToken.userId;
  }

  get userInfo(): any {
    if (!this.decodedToken) {
      return {
        fullName: "",
        email: "",
        initials: "N/A",
      };
    }
    const userInfo = {
      fullName: this.decodedToken.firstName + " " + this.decodedToken.lastName,
      email: this.decodedToken.email,
      initials:
        this.decodedToken.firstName.charAt(0) +
        this.decodedToken.lastName.charAt(0),
    };

    return userInfo;
  }
}
