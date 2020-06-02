import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NumberOfBarsComponent } from './number-of-bars.component';

describe('NumberOfBarsComponent', () => {
  let component: NumberOfBarsComponent;
  let fixture: ComponentFixture<NumberOfBarsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NumberOfBarsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NumberOfBarsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
