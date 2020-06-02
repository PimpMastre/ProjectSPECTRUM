import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChunkMarginsComponent } from './chunk-margins.component';

describe('ChunkMarginsComponent', () => {
  let component: ChunkMarginsComponent;
  let fixture: ComponentFixture<ChunkMarginsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChunkMarginsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChunkMarginsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
