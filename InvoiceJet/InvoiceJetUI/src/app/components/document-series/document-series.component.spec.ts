import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentSeriesComponent } from './document-series.component';

describe('DocumentSeriesComponent', () => {
  let component: DocumentSeriesComponent;
  let fixture: ComponentFixture<DocumentSeriesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DocumentSeriesComponent]
    });
    fixture = TestBed.createComponent(DocumentSeriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
