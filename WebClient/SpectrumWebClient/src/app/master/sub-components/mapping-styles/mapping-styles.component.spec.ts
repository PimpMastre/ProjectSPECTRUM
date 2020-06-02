import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MappingStylesComponent } from './mapping-styles.component';

describe('MappingStylesComponent', () => {
  let component: MappingStylesComponent;
  let fixture: ComponentFixture<MappingStylesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MappingStylesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MappingStylesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
