import { AuthService } from "./../../../services/auth.service";
import { FirmService } from "./../../../services/firm.service";
import { Component, OnInit } from "@angular/core";
import { FormGroup, FormControl, Validators } from "@angular/forms";
import { ToastrService } from "ngx-toastr";
import { IFirm } from "src/app/models/IFirm";

@Component({
  selector: "app-firm-details",
  templateUrl: "./firm-details.component.html",
  styleUrls: ["./firm-details.component.scss"],
})
export class FirmDetailsComponent implements OnInit {
  firmDetailsForm: FormGroup;
  initialFormValues: any;
  currentUserFirm: IFirm | null = null;
  errorMessage: string | null = null;

  constructor(private firmService: FirmService, private toastr: ToastrService) {
    this.firmDetailsForm = new FormGroup({
      firmName: new FormControl("", Validators.required),
      cuiValue: new FormControl("", Validators.required),
      regCom: new FormControl(null),
      address: new FormControl("", Validators.required),
      county: new FormControl("", Validators.required),
      city: new FormControl("", Validators.required),
    });
  }

  ngOnInit(): void {
    this.firmService.getUserActiveFirm().subscribe({
      next: (firm) => {
        if (firm) {
          this.currentUserFirm = firm;
          this.firmDetailsForm.patchValue({
            firmName: firm.name,
            cuiValue: firm.cui,
            regCom: firm.regCom,
            address: firm.address,
            county: firm.county,
            city: firm.city,
          });
        }
      },
    });

    this.initialFormValues = this.firmDetailsForm.value;
  }

  onSubmit(): void {
    if (this.firmDetailsForm.invalid) {
      return;
    }

    const firm: IFirm = {
      id: this.currentUserFirm?.id! ?? 0,
      name: this.firmDetailsForm.value.firmName!,
      cui: this.firmDetailsForm.value.cuiValue!,
      regCom: this.firmDetailsForm.value.regCom! ?? null,
      address: this.firmDetailsForm.value.address!,
      county: this.firmDetailsForm.value.county!,
      city: this.firmDetailsForm.value.city!,
    };

    if (this.firmDetailsForm.valid) {
      if (this.currentUserFirm.id !== 0) {
        this.firmService.editFirm(firm, false).subscribe({
          next: () => {
            this.toastr.success(
              "Firm details updated successfully.",
              "Success"
            );
          },
        });
      } else {
        this.firmService.addFirm(firm, false).subscribe({
          next: () => {
            this.toastr.success(
              "Firm details updated successfully.",
              "Success"
            );
          },
        });
      }
    } else {
      this.errorMessage = "Please fill all the required fields";
    }
  }

  onCloudIconClick(): void {
    this.firmService
      .getFirmFromAnaf(this.firmDetailsForm.value.cuiValue)
      .subscribe({
        next: (firm) => {
          this.firmDetailsForm.patchValue({
            firmName: firm.name,
            regCom: firm.regCom,
            address: firm.address,
            county: firm.county,
            city: firm.city,
          });
          this.toastr.success("Firm details fetched successfully.", "Success");
        },
      });
  }

  isFormChanged(): boolean {
    return (
      JSON.stringify(this.initialFormValues.value) !==
      JSON.stringify(this.initialFormValues)
    );
  }

  addNewClient() {
    console.log("Add new client");
  }
}
