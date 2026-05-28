import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddOrEditInvoiceProformaComponent } from './add-or-edit-invoice-proforma.component';

describe('AddOrEditInvoiceProformaComponent', () => {
  let component: AddOrEditInvoiceProformaComponent;
  let fixture: ComponentFixture<AddOrEditInvoiceProformaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddOrEditInvoiceProformaComponent]
    });
    fixture = TestBed.createComponent(AddOrEditInvoiceProformaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
