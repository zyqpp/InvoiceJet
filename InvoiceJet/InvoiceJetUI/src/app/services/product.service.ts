import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { IProduct } from "../models/IProduct";
import { environment } from "src/environments/environment";

@Injectable({
  providedIn: "root",
})
export class ProductService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  public getProductsForUserId() {
    return this.http.get<IProduct[]>(
      `${this.baseUrl}/Product/GetAllProductsForUserId/`
    );
  }

  public addProduct(product: IProduct) {
    return this.http.post<IProduct>(
      `${this.baseUrl}/Product/AddProduct/`,
      product
    );
  }

  public editProduct(product: IProduct) {
    return this.http.put<IProduct>(
      `${this.baseUrl}/Product/EditProduct/`,
      product
    );
  }

  public deleteProducts(productIds: number[]) {
    return this.http.put(`${this.baseUrl}/Product/DeleteProducts/`, productIds);
  }
}
