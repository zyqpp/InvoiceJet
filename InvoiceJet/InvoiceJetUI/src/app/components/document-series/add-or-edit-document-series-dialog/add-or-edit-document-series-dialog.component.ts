import { Component, Inject, OnInit } from "@angular/core";
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import { ToastrService } from "ngx-toastr";
import { DocumentSeriesService } from "src/app/services/document-series.service";
import { IDocumentSeries } from "src/app/models/IDocumentSeries";

@Component({
  selector: "app-add-or-edit-document-series-dialog",
  templateUrl: "./add-or-edit-document-series-dialog.component.html",
  styleUrls: ["./add-or-edit-document-series-dialog.component.scss"],
})
export class AddOrEditDocumentSeriesDialogComponent implements OnInit {
  documentSeriesForm: FormGroup;
  isEditMode: boolean = false;
  errorMessage: string | null = null;

  documentTypes = [
    { id: 1, name: "Factura" },
    { id: 2, name: "Factura Proforma" },
    { id: 3, name: "Factura Storno" },
  ]; // Adjust as needed

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: IDocumentSeries,
    private dialogRef: MatDialogRef<AddOrEditDocumentSeriesDialogComponent>,
    private documentSeriesService: DocumentSeriesService,
    private toastr: ToastrService
  ) {
    this.documentSeriesForm = new FormGroup({
      id: new FormControl(null),
      documentType: new FormControl(null, Validators.required),
      seriesName: new FormControl("", Validators.required),
      firstNumber: new FormControl("", Validators.required),
      currentNumber: new FormControl("", Validators.required),
      isDefault: new FormControl(false),
    });
  }

  ngOnInit(): void {
    if (this.data) {
      this.isEditMode = true;
      this.documentSeriesForm.setValue({
        id: this.data.id,
        documentType: this.data.documentType.id,
        seriesName: this.data.seriesName,
        firstNumber: this.data.firstNumber,
        currentNumber: this.data.currentNumber,
        isDefault: this.data.isDefault,
      });
    }
  }

  onSubmit(): void {
    if (this.documentSeriesForm.invalid) {
      this.errorMessage = "Please fill in all required fields.";
      return;
    }

    const documentTypeId = this.documentSeriesForm.value.documentType;
    const documentTypeName =
      this.documentTypes.find((type) => type.id === documentTypeId)?.name || "";

    const documentSeriesData: IDocumentSeries = {
      ...this.documentSeriesForm.value,
      documentType: {
        id: documentTypeId,
        name: documentTypeName,
      },
    };

    if (this.isEditMode) {
      this.documentSeriesService
        .updateDocumentSeries(documentSeriesData)
        .subscribe(() => this.handleSuccess());
    } else {
      console.log(documentSeriesData);
      documentSeriesData.id = 0;
      this.documentSeriesService
        .addDocumentSeries(documentSeriesData)
        .subscribe(() => this.handleSuccess());
    }
  }

  handleSuccess(): void {
    this.toastr.success(
      this.isEditMode ? "Document series updated" : "Document series added",
      "Success"
    );
    this.dialogRef.close(true);
  }

  closeDialog(): void {
    this.dialogRef.close(false);
  }
}
