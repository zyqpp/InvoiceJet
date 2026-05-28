import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddOrEditDocumentSeriesDialogComponent } from './add-or-edit-document-series-dialog.component';

describe('AddOrEditDocumentSeriesDialogComponent', () => {
  let component: AddOrEditDocumentSeriesDialogComponent;
  let fixture: ComponentFixture<AddOrEditDocumentSeriesDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddOrEditDocumentSeriesDialogComponent]
    });
    fixture = TestBed.createComponent(AddOrEditDocumentSeriesDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
