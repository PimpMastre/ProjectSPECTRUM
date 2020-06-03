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

  ngOnInit(): void {
    this.bufferLength = this.masterService.settings['previousPeaksBufferLength'];
    this.velocity = this.masterService.settings['velocity'];
  }

  onBufferLengthChanged(event) {
    if(event.target.value < 0) {
      this.bufferLength = 0;
    }

    this.masterService.updateBufferLength(this.bufferLength);
  }

  onVelocityChanged(event) {
    this.masterService.updateVelocity(this.velocity / 100);
  }

  formatVelocity(value) {
    return value + '%';
  }
}
