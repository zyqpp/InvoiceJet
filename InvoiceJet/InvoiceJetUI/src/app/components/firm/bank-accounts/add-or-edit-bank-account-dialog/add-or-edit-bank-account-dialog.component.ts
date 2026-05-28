import { BankAccountService } from "src/app/services/bank-account.service";
import { Component, Inject } from "@angular/core";
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import { MatSnackBar } from "@angular/material/snack-bar";
import { IBankAccount } from "src/app/models/IBankAccount";
import { Currency } from "src/app/enums/Currency";
import { ICurrency } from "src/app/models/ICurrency";
import { ToastrService } from "ngx-toastr";

@Component({
  selector: "app-add-or-edit-bank-account-dialog",
  templateUrl: "./add-or-edit-bank-account-dialog.component.html",
  styleUrls: ["./add-or-edit-bank-account-dialog.component.scss"],
})
export class AddOrEditBankAccountDialogComponent {
  bankAccountForm: FormGroup;
  currencies: ICurrency[] = [
    {
      value: Currency.Ron,
      name: "RON",
    },
    {
      value: Currency.Eur,
      name: "EUR",
    },
  ];
  isEditMode: boolean = false;
  errorMessage: string | null = null;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: IBankAccount,
    private dialogRef: MatDialogRef<AddOrEditBankAccountDialogComponent>,
    private snackBar: MatSnackBar,
    private bankAccountService: BankAccountService,
    private toastr: ToastrService
  ) {
    this.bankAccountForm = new FormGroup({
      id: new FormControl(null),
      bankName: new FormControl("", Validators.required),
      iban: new FormControl("", Validators.required),
      currency: new FormControl(null, Validators.required),
      isActive: new FormControl(false),
    });
  }

  ngOnInit(): void {
    if (this.data) {
      this.isEditMode = true;
      this.bankAccountForm.setValue({
        id: this.data?.id! ?? 0,
        bankName: this.data.bankName,
        iban: this.data.iban,
        currency: this.data.currency,
        isActive: this.data.isActive,
      });
    }
  }

  onSubmit(): void {
    if (this.bankAccountForm.invalid) {
      this.errorMessage = "Please fill in all required fields.";
      return;
    }

    const bankAccountData: IBankAccount = this.bankAccountForm.value;
    bankAccountData.id = this.data?.id! ?? 0;

    if (this.isEditMode) {
      this.bankAccountService
        .editBankAccount(bankAccountData)
        .subscribe(() => this.handleSuccess());
    } else {
      this.bankAccountService
        .addBankAccount(bankAccountData)
        .subscribe(() => this.handleSuccess());
    }
  }

  handleSuccess(): void {
    this.toastr.success(
      this.isEditMode ? "Bank account updated" : "Bank account added",
      "Success"
    );
    this.dialogRef.close(true);
  }

  closeDialog(): void {
    this.dialogRef.close(false);
  }
}
