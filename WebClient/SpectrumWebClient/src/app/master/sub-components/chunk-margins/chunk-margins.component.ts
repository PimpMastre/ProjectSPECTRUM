import { Component, OnInit, ChangeDetectorRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-chunk-margins',
  templateUrl: './chunk-margins.component.html',
  styleUrls: ['./chunk-margins.component.scss']
})
export class ChunkMarginsComponent implements OnInit {
  constructor() { }

  lowerChunkMargin = 0;
  higherChunkMargin = 2048;

  @ViewChild('lowerSlider')lowerSlider;
  @ViewChild('higherSlider')higherSlider;

  ngOnInit(): void {
  }

  onLowerChunkMarginChanged(event) {
    if(event.value > this.higherChunkMargin) {
      this.lowerChunkMargin = this.higherChunkMargin;
    }
    else {
      this.lowerChunkMargin = event.value;
    }

    this.lowerSlider.value = this.lowerChunkMargin;
  }

  onHigherChunkMarginChanged(event) {
    if(event.value < this.lowerChunkMargin) {
      this.higherChunkMargin = this.lowerChunkMargin;
    }
    else {
      this.higherChunkMargin = event.value;
    }

    this.higherSlider.value = this.higherChunkMargin;
  }

  onLowerChunkMarginValueSelected(event) {
    console.log(this.lowerChunkMargin);
  }

  onHigherChunkMarginValueSelected(event) {
    console.log(this.higherChunkMargin);
  }
}
