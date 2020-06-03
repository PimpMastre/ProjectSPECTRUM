import { Component, OnInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import { MasterService } from '../../service/master.service';

@Component({
  selector: 'app-chunk-margins',
  templateUrl: './chunk-margins.component.html',
  styleUrls: ['./chunk-margins.component.scss']
})
export class ChunkMarginsComponent implements OnInit {
  constructor(private masterService: MasterService) { }

  lowerChunkMargin = 0;
  higherChunkMargin = 2048;

  @ViewChild('lowerSlider')lowerSlider;
  @ViewChild('higherSlider')higherSlider;

  ngOnInit(): void {
    this.lowerChunkMargin = this.masterService.settings['lowerChunkMargin'];
    this.higherChunkMargin = this.masterService.settings['higherChunkMargin'];
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
    this.masterService.updateLowerChunkMargin(this.lowerChunkMargin);
  }

  onHigherChunkMarginValueSelected(event) {
    this.masterService.updateHigherChunkMargin(this.higherChunkMargin);
  }
}
