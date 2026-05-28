import { IDocumentProduct } from "./IDocumentProduct";

export interface IDocument {
  id?: number;
  documentNumber: string;
  issueDate: Date;
  dueDate: Date;
  unitPrice: number;
  totalPrice: number;
  documentTypeId: number;
  clientId: number;
  userFirmId: number;
  documentProducts: IDocumentProduct[];
}
