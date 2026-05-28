import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvoiceProformasComponent } from './invoice-proformas.component';

describe('InvoiceProformasComponent', () => {
  let component: InvoiceProformasComponent;
  let fixture: ComponentFixture<InvoiceProformasComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InvoiceProformasComponent]
    });
    fixture = TestBed.createComponent(InvoiceProformasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
