import { IProduct } from "./IProduct";

export interface IDocumentProduct {
  id?: number;
  documentId?: number;
  productId?: number;
  quantity: number;
  product: IProduct;
  document?: Document;
  unitPrice: number;
  totalPrice?: number;
}
