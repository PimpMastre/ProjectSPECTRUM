import { Component, OnInit } from '@angular/core';
import { SlaveService } from '../../service/slave.service';

@Component({
  selector: 'app-led-falloff',
  templateUrl: './led-falloff.component.html',
  styleUrls: ['./led-falloff.component.scss']
})
export class LedFalloffComponent implements OnInit {

  constructor(private slaveService: SlaveService) { }

  ledFalloff = 0;

  ngOnInit(): void {
    this.ledFalloff = this.slaveService.settings['ledFalloff'];
  }

  onFalloffChanged(event) {
    if(event.target.value < 0) {
      this.ledFalloff = 0;
    }

    this.slaveService.updateLedFalloff(this.ledFalloff);
  }
}
