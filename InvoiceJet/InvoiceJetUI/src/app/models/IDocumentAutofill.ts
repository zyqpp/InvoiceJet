import { IDocumentSeries } from "./IDocumentSeries";
import { IDocumentStatus } from "./IDocumentStatus";
import { IFirm } from "./IFirm";
import { IProduct } from "./IProduct";

export interface IDocumentAutofill {
  clients: IFirm[];
  documentSeries: IDocumentSeries[];
  documentStatuses: IDocumentStatus[];
  products: IProduct[];
}
