import { Component, OnInit } from '@angular/core';
import { MasterService } from '../../service/master.service';

@Component({
  selector: 'app-buffers',
  templateUrl: './buffers.component.html',
  styleUrls: ['./buffers.component.scss']
})
export class BuffersComponent implements OnInit {

  constructor(private masterService: MasterService) { }

  public bufferLength = 2;
  public velocity = 33;
  public dataAveraging = 10;

  ngOnInit(): void {
    this.bufferLength = this.masterService.settings['previousPeaksBufferLength'];
    this.velocity = this.masterService.settings['velocity'] * 100;
    this.dataAveraging = this.masterService.settings['dataAveraging'];
  }

  onBufferLengthChanged(event) {
    if(event.target.value < 0) {
      this.bufferLength = 0;
    }

    this.masterService.updateBufferLength(this.bufferLength);
  }
  
  onDataAveragingChanged(event) {
    this.dataAveraging = event.value;

    this.masterService.updateDataAveraging(this.dataAveraging);
  }

  onVelocityChanged(event) {
    this.masterService.updateVelocity(this.velocity / 100);
  }

  formatVelocity(value) {
    return value + '%';
  }

  formatDataAveraging(value) {
    return value + "%";
  }
}
