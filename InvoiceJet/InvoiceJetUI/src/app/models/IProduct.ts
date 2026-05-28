export interface IProduct {
  id?: number;
  name: string;
  price: number;
  containsTva: boolean;
  unitOfMeasurement: string;
  tvaValue: number;
}
