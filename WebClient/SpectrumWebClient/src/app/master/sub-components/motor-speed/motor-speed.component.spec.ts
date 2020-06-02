import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MotorSpeedComponent } from './motor-speed.component';

describe('MotorSpeedComponent', () => {
  let component: MotorSpeedComponent;
  let fixture: ComponentFixture<MotorSpeedComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MotorSpeedComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MotorSpeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
