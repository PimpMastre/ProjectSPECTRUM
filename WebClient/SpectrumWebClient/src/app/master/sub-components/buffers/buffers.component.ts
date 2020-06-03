import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-buffers',
  templateUrl: './buffers.component.html',
  styleUrls: ['./buffers.component.scss']
})
export class BuffersComponent implements OnInit {

  constructor() { }

  public bufferLength = 2;
  public velocity = 33;

  ngOnInit(): void {

  }

  onBufferLengthChanged(event) {
    if(event.target.value < 0) {
      this.bufferLength = 0;
    }
  }

  onVelocityChanged(event) {
    console.log(this.velocity / 100);
  }

  formatVelocity(value) {
    return value + '%';
  }
}
