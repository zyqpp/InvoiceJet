import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvoiceStornosComponent } from './invoice-stornos.component';

describe('InvoiceStornosComponent', () => {
  let component: InvoiceStornosComponent;
  let fixture: ComponentFixture<InvoiceStornosComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InvoiceStornosComponent]
    });
    fixture = TestBed.createComponent(InvoiceStornosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
