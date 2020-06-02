import { Component, OnInit, ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-chunk-margins',
  templateUrl: './chunk-margins.component.html',
  styleUrls: ['./chunk-margins.component.scss']
})
export class ChunkMarginsComponent implements OnInit {
  constructor(private cdr: ChangeDetectorRef) { }

  lowerChunkMargin = 0;
  higherChunkMargin = 2048;

  ngOnInit(): void {
  }

  onLowerValueChanged(event) {
    console.log(event);
    this.lowerChunkMargin = event.value;
  }

  onHigherValueChanged(event) {
    console.log(event);
    this.higherChunkMargin = event.value;
    this.cdr.detectChanges();
  }
}
