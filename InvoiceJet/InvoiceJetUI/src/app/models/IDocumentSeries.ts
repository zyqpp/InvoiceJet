import { IDocumentType } from "./IDocumentType";

export interface IDocumentSeries {
  id: number;
  seriesName: string;
  firstNumber: number;
  currentNumber: number;
  isDefault: boolean;
  documentTypeId: number;
  documentType: IDocumentType;
}
