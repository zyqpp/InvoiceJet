import { AuthService } from "src/app/services/auth.service";
import { Component } from "@angular/core";
import { NavigationEnd, Router } from "@angular/router";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
})
export class AppComponent {
  title = "InvoiceJet";
  isLoginOrRegister = false;

  constructor(private authService: AuthService, private router: Router) {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.isLoginOrRegister =
          !event.url.includes("login") && !event.url.includes("register");
      }
    });
  }
}
