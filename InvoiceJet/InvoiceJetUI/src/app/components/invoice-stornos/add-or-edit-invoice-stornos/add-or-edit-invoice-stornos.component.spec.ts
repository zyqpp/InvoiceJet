import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddOrEditInvoiceStornosComponent } from './add-or-edit-invoice-stornos.component';

describe('AddOrEditInvoiceStornosComponent', () => {
  let component: AddOrEditInvoiceStornosComponent;
  let fixture: ComponentFixture<AddOrEditInvoiceStornosComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddOrEditInvoiceStornosComponent]
    });
    fixture = TestBed.createComponent(AddOrEditInvoiceStornosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
