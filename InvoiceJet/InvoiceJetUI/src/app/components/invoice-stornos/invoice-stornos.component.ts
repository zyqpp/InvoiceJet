import { SelectionModel } from "@angular/cdk/collections";
import { AfterViewInit, Component, ViewChild } from "@angular/core";
import { MatTableDataSource } from "@angular/material/table";
import { MatPaginator } from "@angular/material/paginator";
import { MatSort } from "@angular/material/sort";
import { Router } from "@angular/router";
import { IDocumentTableRecord } from "src/app/models/IDocumentTableRecord";
import { DocumentService } from "src/app/services/document.service";

@Component({
  selector: "app-invoice-stornos",
  templateUrl: "./invoice-stornos.component.html",
  styleUrls: ["./invoice-stornos.component.scss"],
})
export class InvoiceStornosComponent implements AfterViewInit {
  displayedColumns: string[] = [
    "select",
    "documentNumber",
    "clientName",
    "issueDate",
    "dueDate",
    "totalValue",
    "documentStatus",
  ];
  dataSource = new MatTableDataSource<IDocumentTableRecord>([]);
  selection = new SelectionModel<IDocumentTableRecord>(true, []);
  invoices: IDocumentTableRecord[] = [];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private router: Router,
    private documentService: DocumentService
  ) {}

  ngOnInit() {
    this.loadInvoices();
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  loadInvoices(): void {
    this.documentService.getDocuments(3).subscribe((invoices) => {
      this.dataSource.data = invoices;
      this.invoices = invoices;
      console.log(this.invoices);
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  masterToggle() {
    if (this.isAllSelected()) {
      this.selection.clear();
    } else {
      this.dataSource.data.forEach((row) => this.selection.select(row));
    }
  }

  openEditInvoiceStornoDialog(row: IDocumentTableRecord): void {
    this.router.navigate(["/dashboard/edit-invoice-storno", row.id]);
  }

  deleteSelected(): void {
    console.log(this.selection.selected);

    const documentIds: number[] = this.selection.selected.map((doc) => doc.id);
    console.log(documentIds);
    this.documentService.deleteDocuments(documentIds).subscribe({
      next: () => {
        this.loadInvoices();
      },
      error: (err) => {
        console.error("Error deleting documents", err);
      },
    });
  }

  clearSearch(input: HTMLInputElement) {
    input.value = "";
    this.dataSource.filter = "";
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}
