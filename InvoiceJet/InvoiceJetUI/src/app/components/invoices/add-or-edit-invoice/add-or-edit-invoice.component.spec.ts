import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddOrEditInvoiceComponent } from './add-or-edit-invoice.component';

describe('AddOrEditInvoiceComponent', () => {
  let component: AddOrEditInvoiceComponent;
  let fixture: ComponentFixture<AddOrEditInvoiceComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddOrEditInvoiceComponent]
    });
    fixture = TestBed.createComponent(AddOrEditInvoiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
