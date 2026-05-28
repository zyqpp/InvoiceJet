import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TokenExpiredDialogComponent } from './token-expired-dialog.component';

describe('TokenExpiredDialogComponent', () => {
  let component: TokenExpiredDialogComponent;
  let fixture: ComponentFixture<TokenExpiredDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TokenExpiredDialogComponent]
    });
    fixture = TestBed.createComponent(TokenExpiredDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
