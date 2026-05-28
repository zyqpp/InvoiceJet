import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";
import { IDocumentSeries } from "../models/IDocumentSeries";

@Injectable({
  providedIn: "root",
})
export class DocumentSeriesService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  public getDocumentSeriesForUserId() {
    return this.http.get<IDocumentSeries[]>(
      `${this.baseUrl}/DocumentSeries/GetAllDocumentSeriesForUserId`
    );
  }

  public addDocumentSeries(documentSeries: IDocumentSeries) {
    return this.http.post<IDocumentSeries>(
      `${this.baseUrl}/DocumentSeries/AddDocumentSeries`,
      documentSeries
    );
  }

  public updateDocumentSeries(documentSeries: IDocumentSeries) {
    return this.http.put<IDocumentSeries>(
      `${this.baseUrl}/DocumentSeries/UpdateDocumentSeries`,
      documentSeries
    );
  }

  deleteDocumentSeries(documentIds: number[]) {
    return this.http.put(
      `${this.baseUrl}/DocumentSeries/DeleteDocumentSeries`,
      documentIds
    );
  }
}
