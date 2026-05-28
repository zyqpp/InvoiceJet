import { Injectable } from "@angular/core";
import { MatDialog } from "@angular/material/dialog";
import {
  ActivatedRouteSnapshot,
  CanActivate,
  Router,
  RouterStateSnapshot,
  UrlTree,
} from "@angular/router";
import { Observable } from "rxjs";
import { AuthService } from "src/app/services/auth.service";

@Injectable({
  providedIn: "root",
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ):
    | boolean
    | UrlTree
    | Observable<boolean | UrlTree>
    | Promise<boolean | UrlTree> {
    return this.checkAuthentication(state.url);
  }

  private checkAuthentication(url: string): boolean | UrlTree {
    if (this.authService.isLoggedIn()) {
      return true;
    } else {
      this.authService.logout();
      this.router.navigate(["/login"]);
      return false;
    }
  }
}
