import { ToastrService } from "ngx-toastr";
import { ProductService } from "src/app/services/product.service";
import { Component, Inject, OnInit } from "@angular/core";
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { IProduct } from "src/app/models/IProduct";
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";

@Component({
  selector: "app-add-or-edit-product-dialog",
  templateUrl: "./add-or-edit-product-dialog.component.html",
  styleUrls: ["./add-or-edit-product-dialog.component.scss"],
})
export class AddOrEditProductDialogComponent implements OnInit {
  productForm!: FormGroup;
  isEditMode: boolean = false;
  errorMessage!: string;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: IProduct,
    private productService: ProductService,
    private dialogRef: MatDialogRef<AddOrEditProductDialogComponent>,
    private toastr: ToastrService
  ) {
    this.productForm = new FormGroup({
      id: new FormControl(null),
      name: new FormControl("", Validators.required),
      price: new FormControl("", Validators.required),
      containsTva: new FormControl(false),
      tvaValue: new FormControl(19, Validators.required),
      unitOfMeasurement: new FormControl(""),
    });
  }

  ngOnInit(): void {
    if (this.data) {
      this.isEditMode = true;
      this.productForm.setValue({
        id: this.data?.id! ?? 0,
        name: this.data.name,
        price: this.data.price,
        containsTva: this.data.containsTva,
        tvaValue: this.data.tvaValue,
        unitOfMeasurement: this.data.unitOfMeasurement,
      });
    }
  }

  initForm(): void {}

  onSubmit(): void {
    if (this.productForm.valid) {
      const productData: IProduct = this.productForm.value;
      productData.id = this.data?.id! ?? 0;

      if (this.isEditMode) {
        this.productService.editProduct(productData).subscribe({
          next: () => {
            this.toastr.success("Product updated successfully!");
            this.dialogRef.close(true);
          },
        });
      } else {
        this.productService.addProduct(productData).subscribe({
          next: () => {
            this.toastr.success("Product added successfully!");
            this.dialogRef.close(true);
          },
        });
      }
    } else {
      this.errorMessage = "Please fill in all required fields.";
    }
  }

  closeDialog() {
    this.dialogRef.close(false);
  }
}
