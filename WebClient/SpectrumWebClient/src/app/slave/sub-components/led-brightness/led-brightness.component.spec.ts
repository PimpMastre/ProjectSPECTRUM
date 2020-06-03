import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LedBrightnessComponent } from './led-brightness.component';

describe('LedBrightnessComponent', () => {
  let component: LedBrightnessComponent;
  let fixture: ComponentFixture<LedBrightnessComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LedBrightnessComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LedBrightnessComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
