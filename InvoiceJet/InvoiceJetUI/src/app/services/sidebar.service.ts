import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class SidebarService {
  private _sidebarVisible: BehaviorSubject<boolean>;

  constructor() {
    const isLargeScreen = window.innerWidth > 1500;
    this._sidebarVisible = new BehaviorSubject<boolean>(isLargeScreen);
    this.sidebarVisible = this._sidebarVisible.asObservable();
  }

  sidebarVisible: Observable<boolean>;

  toggleSidebar() {
    this._sidebarVisible.next(!this._sidebarVisible.value);
  }
}
