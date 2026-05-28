import { DocumentSeriesService } from "./../../services/document-series.service";
import { LiveAnnouncer } from "@angular/cdk/a11y";
import { SelectionModel } from "@angular/cdk/collections";
import { Component, OnInit, ViewChild } from "@angular/core";
import { MatDialog } from "@angular/material/dialog";
import { MatSort } from "@angular/material/sort";
import { MatTableDataSource } from "@angular/material/table";
import { MatPaginator } from "@angular/material/paginator";
import { IDocumentSeries } from "src/app/models/IDocumentSeries";
import { AddOrEditDocumentSeriesDialogComponent } from "./add-or-edit-document-series-dialog/add-or-edit-document-series-dialog.component";
import { ToastrService } from "ngx-toastr";

@Component({
  selector: "app-document-series",
  templateUrl: "./document-series.component.html",
  styleUrls: ["./document-series.component.scss"],
})
export class DocumentSeriesComponent implements OnInit {
  displayedColumns: string[] = [
    "select",
    "documentType",
    "seriesName",
    "firstNumber",
    "currentNumber",
    "isDefault",
  ];
  dataSource = new MatTableDataSource<IDocumentSeries>();
  selection = new SelectionModel<IDocumentSeries>(true, []);
  documentSeriesList!: IDocumentSeries[];

  constructor(
    public dialog: MatDialog,
    private documentSeriesService: DocumentSeriesService,
    private _liveAnnouncer: LiveAnnouncer,
    private toastr: ToastrService
  ) {}

  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  ngOnInit(): void {
    this.getDocumentSeries();
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
  }

  getDocumentSeries(): void {
    this.documentSeriesService
      .getDocumentSeriesForUserId()
      .subscribe((series) => {
        console.log(series);
        this.documentSeriesList = series;
        this.dataSource.data = this.documentSeriesList;
      });
  }

  openNewDocumentSeriesDialog() {
    const dialogRef = this.dialog.open(AddOrEditDocumentSeriesDialogComponent, {
      panelClass: "custom-dialog-panel",
      data: null,
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.getDocumentSeries();
      }
    });
  }

  openEditDocumentSeriesDialog(row: IDocumentSeries) {
    const dialogRef = this.dialog.open(AddOrEditDocumentSeriesDialogComponent, {
      data: row,
      panelClass: "custom-dialog-panel",
      disableClose: true,
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.getDocumentSeries();
      }
    });
  }

  announceSortChange(sortState: any) {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce("Sorting cleared");
    }
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  clearSearch(input: HTMLInputElement) {
    input.value = "";
    this.dataSource.filter = "";
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
    this.isAllSelected()
      ? this.selection.clear()
      : this.dataSource.data.forEach((row) => this.selection.select(row));
  }

  deleteSelected() {
    const selectedIds = this.selection.selected.map((s) => s.id); // Get IDs of selected items
    console.log(selectedIds);
    this.documentSeriesService
      .deleteDocumentSeries(selectedIds)
      .subscribe(() => {
        this.getDocumentSeries();
        this.selection.clear();
        this.toastr.success("Document series deleted successfully.", "Success");
      });
    this.selection.clear();
  }
}
