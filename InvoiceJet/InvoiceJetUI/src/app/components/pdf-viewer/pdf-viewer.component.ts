import { Component, Inject } from "@angular/core";
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import { DomSanitizer, SafeResourceUrl } from "@angular/platform-browser";

@Component({
  selector: "app-pdf-viewer",
  templateUrl: "./pdf-viewer.component.html",
  styleUrls: ["./pdf-viewer.component.scss"],
})
export class PdfViewerComponent {
  public safeUrl: SafeResourceUrl;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { pdfUrl: string },
    private dialogRef: MatDialogRef<PdfViewerComponent>,
    private sanitizer: DomSanitizer
  ) {
    this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(data.pdfUrl);
  }

  ngOnInit(): void {}

  onClose(): void {
    this.dialogRef.close(); // This will close the dialog
  }
}
