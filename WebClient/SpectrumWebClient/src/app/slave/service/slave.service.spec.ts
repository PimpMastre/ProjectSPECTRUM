import { TestBed } from '@angular/core/testing';

import { SlaveService } from './slave.service';

describe('SlaveService', () => {
  let service: SlaveService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SlaveService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
