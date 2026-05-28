import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddOrEditBankAccountDialogComponent } from './add-or-edit-bank-account-dialog.component';

describe('AddOrEditBankAccountDialogComponent', () => {
  let component: AddOrEditBankAccountDialogComponent;
  let fixture: ComponentFixture<AddOrEditBankAccountDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddOrEditBankAccountDialogComponent]
    });
    fixture = TestBed.createComponent(AddOrEditBankAccountDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
