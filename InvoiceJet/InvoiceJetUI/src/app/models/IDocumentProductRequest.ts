import { IProduct } from "./IProduct";

export interface IDocumentProductRequest {
  id?: 0;
  name: string;
  unitPrice: number;
  totalPrice: number;
  containsTva: boolean;
  unitOfMeasurement: string;
  tvaValue: number;
  quantity: number;
}
