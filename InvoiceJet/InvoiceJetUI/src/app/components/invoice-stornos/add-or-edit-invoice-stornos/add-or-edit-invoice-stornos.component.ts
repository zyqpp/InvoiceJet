import { Component } from "@angular/core";
import { BaseInvoiceComponent } from "../../invoices/base-invoice/base-invoice.component";

@Component({
  selector: "app-add-or-edit-invoice-stornos",
  templateUrl: "./add-or-edit-invoice-stornos.component.html",
  styleUrls: ["./add-or-edit-invoice-stornos.component.scss"],
})
export class AddOrEditInvoiceStornosComponent extends BaseInvoiceComponent {
  getDocumentTypeId(): number {
    return 3;
  }

  getNavigationUrl(): string {
    return "/dashboard/invoice-stornos";
  }
}
