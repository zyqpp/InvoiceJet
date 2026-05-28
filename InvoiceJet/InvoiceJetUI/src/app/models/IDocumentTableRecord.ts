import { IDocumentStatus } from "./IDocumentStatus";

export interface IDocumentTableRecord {
  id: number;
  documentNumber: string;
  clientName: string;
  issueDate: Date;
  dueDate: Date;
  totalValue: number;
  documentStatus: IDocumentStatus;
}
