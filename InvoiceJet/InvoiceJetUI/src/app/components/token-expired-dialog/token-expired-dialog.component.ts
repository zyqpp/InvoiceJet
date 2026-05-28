import { AuthService } from "src/app/services/auth.service";
import { Component } from "@angular/core";
import { MatDialogRef } from "@angular/material/dialog";
import { Route, Router } from "@angular/router";

@Component({
  selector: "app-token-expired-dialog",
  templateUrl: "./token-expired-dialog.component.html",
  styleUrls: ["./token-expired-dialog.component.scss"],
})
export class TokenExpiredDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<TokenExpiredDialogComponent>,
    private router: Router,
    private authService: AuthService
  ) {}

  logIn(): void {
    this.router.navigate(["/login"]);
    this.dialogRef.close();
  }
}
