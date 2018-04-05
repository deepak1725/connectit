import { TestBed, async, inject } from '@angular/core/testing';

import { BouncerGuard } from './bouncer.guard';

describe('BouncerGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [BouncerGuard]
    });
  });

  it('should ...', inject([BouncerGuard], (guard: BouncerGuard) => {
    expect(guard).toBeTruthy();
  }));
});
