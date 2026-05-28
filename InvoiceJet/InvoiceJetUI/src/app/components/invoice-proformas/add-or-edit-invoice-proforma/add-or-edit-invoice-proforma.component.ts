import { Component } from "@angular/core";
import { BaseInvoiceComponent } from "../../invoices/base-invoice/base-invoice.component";
@Component({
  selector: "app-add-or-edit-invoice-proforma",
  templateUrl: "./add-or-edit-invoice-proforma.component.html",
  styleUrls: ["./add-or-edit-invoice-proforma.component.scss"],
})
export class AddOrEditInvoiceProformaComponent extends BaseInvoiceComponent {
  getDocumentTypeId(): number {
    return 2;
  }

  getNavigationUrl(): string {
    return "/dashboard/invoice-proformas";
  }
}
