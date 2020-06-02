import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LedFalloffComponent } from './led-falloff.component';

describe('LedFalloffComponent', () => {
  let component: LedFalloffComponent;
  let fixture: ComponentFixture<LedFalloffComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LedFalloffComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LedFalloffComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
