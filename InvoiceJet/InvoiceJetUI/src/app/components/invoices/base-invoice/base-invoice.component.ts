import {
  ChangeDetectorRef,
  Component,
  OnInit,
  AfterViewInit,
} from "@angular/core";
import { FormArray, FormBuilder, FormGroup, Validators } from "@angular/forms";
import { MatTableDataSource } from "@angular/material/table";
import { Observable, map, merge, startWith } from "rxjs";
import { IFirm } from "src/app/models/IFirm";
import { IDocumentAutofill } from "src/app/models/IDocumentAutofill";
import { IProduct } from "src/app/models/IProduct";
import { IDocumentRequest } from "src/app/models/IDocumentRequest";
import { ActivatedRoute, Router } from "@angular/router";
import { DocumentService } from "src/app/services/document.service";
import { MatDialog } from "@angular/material/dialog";
import { ToastrService } from "ngx-toastr";
import { PdfViewerComponent } from "../../pdf-viewer/pdf-viewer.component";
import { IDocumentStatus } from "src/app/models/IDocumentStatus";
import { dueDateValidator } from "./date-validator";

@Component({
  selector: "app-base-invoice",
  template: "",
})
export abstract class BaseInvoiceComponent implements OnInit, AfterViewInit {
  invoiceAutofillData: IDocumentAutofill = {} as IDocumentAutofill;
  filteredFirms!: Observable<IFirm[]>;
  filteredProducts!: Observable<IProduct[]>;
  currentDocument!: IDocumentRequest;
  currentStatus!: IDocumentStatus;
  loading = true;
  isEditMode = false;

  dataSource = new MatTableDataSource();
  invoiceForm: FormGroup = {} as FormGroup;
  displayedColumns: string[] = [
    "name",
    "unitPrice",
    "quantity",
    "unitOfMeasurement",
    "tvaValue",
    "containsTva",
    "totalPrice",
    "actions",
  ];

  constructor(
    protected fb: FormBuilder,
    protected documentService: DocumentService,
    protected dialog: MatDialog,
    protected router: Router,
    protected route: ActivatedRoute,
    protected toastr: ToastrService,
    protected cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.initializeForm();

    this.route.params.subscribe((params) => {
      const invoiceId = +params["id"];
      this.isEditMode = !!invoiceId;
      this.loadAutofillData(invoiceId);
    });
  }

  initializeForm(): void {
    this.invoiceForm = this.fb.group({
      id: 0,
      client: [null, Validators.required],
      issueDate: [new Date(), Validators.required],
      dueDate: [null, dueDateValidator],
      documentSeries: [null],
      documentStatus: [null],
      products: this.fb.array([this.createProductGroup()]),
    });
    this.updateTableData();
  }

  loadAutofillData(invoiceId: number | undefined): void {
    this.documentService
      .getDocumentAutofillInfo(this.getDocumentTypeId())
      .subscribe({
        next: (autofillData) => {
          this.invoiceAutofillData = autofillData;

          if (invoiceId) {
            this.loadDocument(invoiceId);
          } else {
            this.setupClientFilters();
            this.setupProductFilters();
            this.loading = false;
          }
        },
      });
  }

  loadDocument(invoiceId: number): void {
    this.documentService.getDocumentById(invoiceId).subscribe({
      next: (documentData) => {
        this.currentDocument = documentData;

        this.patchFormData();
        this.updateTableData();
        this.setupClientFilters();
        this.setupProductFilters();
        this.loading = false;
      },
      error: (err) => {
        console.error("Error loading document data", err);
      },
    });
  }

  patchFormData(): void {
    if (this.currentDocument) {
      this.invoiceForm.patchValue(this.currentDocument);
      this.invoiceForm.setControl(
        "products",
        this.fb.array(
          this.currentDocument.products.map((product) => this.fb.group(product))
        )
      );
      const documentStatus = this.invoiceAutofillData.documentStatuses.find(
        (status) => status.id === this.currentDocument.documentStatus.id
      );
      if (documentStatus) {
        this.invoiceForm.patchValue({ documentStatus: documentStatus });
      }
      this.cdr.detectChanges();
    }
  }

  ngAfterViewInit(): void {
    if (this.currentDocument) {
      this.patchFormData();
    }
  }

  displayFn(firm: IFirm): string {
    return firm && firm.name ? firm.name : "";
  }

  setupClientFilters() {
    this.filteredFirms = this.invoiceForm.get("client")!.valueChanges.pipe(
      startWith(""),
      map((value) => this.filterClients(value))
    );
  }

  setupProductFilters() {
    const products = this.productsFormArray;
    if (products.length === 0) return;

    const nameChangeObservables: Observable<any>[] = products.controls.map(
      (productFormGroup) => {
        return productFormGroup.get("name")!.valueChanges.pipe(
          startWith(""),
          map((value) => this.filterProducts(value))
        );
      }
    );

    this.filteredProducts = merge(...nameChangeObservables);
  }

  filterClients(value: any): IFirm[] {
    let filterValue = "";

    if (typeof value === "string") {
      filterValue = value.toLowerCase();
    } else if (value && typeof value === "object" && value.name) {
      filterValue = value.name.toLowerCase();
    }

    return this.invoiceAutofillData.clients.filter(
      (firm) =>
        firm.name.toLowerCase().includes(filterValue) ||
        firm.cui.toLowerCase().includes(filterValue)
    );
  }

  filterProducts(value: string): any[] {
    console.log("Filtering products", value);
    const filterValue = value.toLowerCase();
    return this.invoiceAutofillData.products.filter((product) =>
      product.name.toLowerCase().includes(filterValue)
    );
  }

  updateTableData() {
    this.dataSource.data = this.getControls();
  }

  createProductGroup(): FormGroup {
    return this.fb.group({
      id: 0,
      name: [null, Validators.required],
      unitPrice: [null, [Validators.required, Validators.min(0)]],
      totalPrice: [null, [Validators.required, Validators.min(0)]],
      quantity: [1, [Validators.required, Validators.min(1)]],
      unitOfMeasurement: ["buc", Validators.required],
      tvaValue: [19, [Validators.required, Validators.min(0)]],
      containsTva: [false],
    });
  }

  get productsFormArray(): FormArray {
    return this.invoiceForm.get("products") as FormArray;
  }

  getControls() {
    return (this.invoiceForm.get("products") as FormArray).controls;
  }

  addProduct(): void {
    console.log(this.productsFormArray.value);
    this.productsFormArray.push(this.createProductGroup());
    this.updateTableData();
    this.setupProductFilters();
  }

  deleteProduct(index: number): void {
    this.productsFormArray.removeAt(index);
    this.updateTableData();
  }

  onProductSelected(event: any, index: number): void {
    const selectedProduct = this.invoiceAutofillData.products.find(
      (product) => product.name === event.option.value
    );
    if (selectedProduct) {
      const productGroup = this.productsFormArray.at(index) as FormGroup;
      productGroup.patchValue({
        id: selectedProduct.id,
        unitPrice: selectedProduct.price,
        unitOfMeasurement: selectedProduct.unitOfMeasurement,
        tvaValue: selectedProduct.tvaValue,
        containsTva: selectedProduct.containsTva,
      });
      this.calculateTotalPrice(index);
    }
  }

  calculateTotalPrice(index: number): void {
    const productGroup = this.productsFormArray.at(index) as FormGroup;
    const unitPrice = parseFloat(productGroup.get("unitPrice")!.value);
    const quantity = parseFloat(productGroup.get("quantity")!.value);
    const tvaValue = parseFloat(productGroup.get("tvaValue")!.value);

    const totalPrice = unitPrice * quantity;
    const tva = totalPrice * (tvaValue / 100);
    const finalPrice = totalPrice + tva;

    const finalPriceRounded = parseFloat(finalPrice.toFixed(2));

    productGroup.patchValue({
      totalPrice: finalPriceRounded,
    });
  }

  calculatePriceWithoutTVA(index: number, isChecked: boolean): void {
    console.log("Checkbox checked", isChecked);

    const productGroup = this.productsFormArray.at(index) as FormGroup;
    const unitPrice = parseFloat(productGroup.get("unitPrice")!.value);
    const quantity = parseFloat(productGroup.get("quantity")!.value);
    const tvaValue = parseFloat(productGroup.get("tvaValue")!.value);

    if (isChecked) {
      const newTotalPrice = unitPrice * quantity;
      const newUnitPrice = newTotalPrice / quantity / (1 + tvaValue / 100);

      productGroup.patchValue({
        unitPrice: parseFloat(newUnitPrice.toFixed(2)),
        totalPrice: parseFloat(newTotalPrice.toFixed(2)),
      });
    } else {
      const unitPrice = parseFloat(productGroup.get("unitPrice").value);
      const quantity = parseFloat(productGroup.get("quantity").value);
      const tvaValue = parseFloat(productGroup.get("tvaValue").value);

      const originalUnitPrice = unitPrice * (1 + tvaValue / 100);
      const originalTotalPrice =
        originalUnitPrice * quantity +
        (originalUnitPrice * quantity * tvaValue) / 100;

      productGroup.patchValue({
        unitPrice: parseFloat(originalUnitPrice.toFixed(2)),
        totalPrice: parseFloat(originalTotalPrice.toFixed(2)),
      });
    }
  }

  abstract getDocumentTypeId(): number;

  onSubmit(): void {
    if (this.invoiceForm.invalid) return;

    const documentData: IDocumentRequest = this.invoiceForm.value;
    documentData.documentType = { id: this.getDocumentTypeId(), name: "" };

    if (this.isEditMode) {
      this.updateDocument(documentData);
    } else {
      this.addDocument(documentData);
    }
  }

  updateDocument(documentData: IDocumentRequest) {
    this.documentService.updateDocument(documentData).subscribe({
      next: () => {
        this.toastr.success("Document updated successfully");
        this.router.navigateByUrl(this.getNavigationUrl());
      },
    });
  }

  addDocument(documentData: IDocumentRequest) {
    this.documentService.addDocument(documentData).subscribe({
      next: () => {
        this.toastr.success("Document added successfully");
        this.router.navigateByUrl(this.getNavigationUrl());
      },
    });
  }

  abstract getNavigationUrl(): string;

  generateInvoicePdf() {
    const documentData: IDocumentRequest = this.invoiceForm.value;

    this.documentService.generateDocumentPdf(documentData).subscribe({
      next: () => {
        console.log("Invoice pdf generated successfully");
      },
    });
  }

  getInvoicePdfStream() {
    // if (this.invoiceForm.invalid) return;

    const documentData: IDocumentRequest = this.invoiceForm.value;
    documentData.documentType = { id: this.getDocumentTypeId(), name: "" };
    documentData.documentNumber = this.currentDocument.documentNumber;
    documentData.documentStatus = this.currentDocument.documentStatus;

    this.documentService.getGeneratedDocumentPdf(documentData).subscribe({
      next: (data) => {
        const blob = new Blob([data], { type: "application/pdf" });
        const url = window.URL.createObjectURL(blob);

        this.dialog.open(PdfViewerComponent, {
          data: { pdfUrl: url },
          width: "100vw",
          height: "90vh",
          disableClose: true,
        });
      },
      error: (err) => {
        console.error("Error getting invoice pdf stream", err);
      },
    });
  }

  goBack(): void {
    this.router.navigateByUrl(this.getNavigationUrl());
  }

  get documentNumber(): string {
    return this.currentDocument?.documentNumber || "";
  }

  get documentStatus(): string {
    return this.currentDocument?.documentStatus?.status || "";
  }
}
