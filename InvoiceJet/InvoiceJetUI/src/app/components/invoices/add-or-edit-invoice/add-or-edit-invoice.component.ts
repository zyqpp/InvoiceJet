import { Component } from "@angular/core";
import { BaseInvoiceComponent } from "../base-invoice/base-invoice.component";

@Component({
  selector: "app-add-or-edit-invoice",
  templateUrl: "./add-or-edit-invoice.component.html",
  styleUrls: ["./add-or-edit-invoice.component.scss"],
})
export class AddOrEditInvoiceComponent extends BaseInvoiceComponent {
  getDocumentTypeId(): number {
    return 1;
  }

  getNavigationUrl(): string {
    return "/dashboard/invoices";
  }
}
