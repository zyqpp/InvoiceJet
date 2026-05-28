import { Component } from "@angular/core";
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { Router } from "@angular/router";
import { ILoginUser } from "src/app/models/ILoginUser";
import { AuthService } from "src/app/services/auth.service";

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
  styleUrls: ["./login.component.scss"],
})
export class LoginComponent {
  errorMessage: string | null = null;
  hide = true;

  loginForm = new FormGroup({
    email: new FormControl("", [Validators.required, Validators.email]),
    password: new FormControl("", Validators.required),
  });

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit(): void {
    if (this.loginForm.valid) {
      const user: ILoginUser = {
        email: this.loginForm.value.email!,
        password: this.loginForm.value.password!,
      };

      this.authService.login(user).subscribe({
        next: (response: { token: string }) => {
          localStorage.setItem("authToken", response.token);
          this.router.navigate(["dashboard"]);
        },
      });
    }
  }
}
