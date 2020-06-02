import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AmplitudeSettingsComponent } from './amplitude-settings.component';

describe('AmplitudeSettingsComponent', () => {
  let component: AmplitudeSettingsComponent;
  let fixture: ComponentFixture<AmplitudeSettingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AmplitudeSettingsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AmplitudeSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
