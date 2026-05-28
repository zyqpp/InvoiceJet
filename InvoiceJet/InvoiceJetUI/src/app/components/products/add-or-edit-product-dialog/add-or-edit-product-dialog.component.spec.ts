import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddOrEditProductDialogComponent } from './add-or-edit-product-dialog.component';

describe('AddOrEditProductDialogComponent', () => {
  let component: AddOrEditProductDialogComponent;
  let fixture: ComponentFixture<AddOrEditProductDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddOrEditProductDialogComponent]
    });
    fixture = TestBed.createComponent(AddOrEditProductDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
