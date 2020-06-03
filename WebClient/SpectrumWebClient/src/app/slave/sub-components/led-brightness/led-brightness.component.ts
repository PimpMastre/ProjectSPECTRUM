import { Component, OnInit } from '@angular/core';
import { SlaveService } from '../../service/slave.service';

@Component({
  selector: 'app-led-brightness',
  templateUrl: './led-brightness.component.html',
  styleUrls: ['./led-brightness.component.scss']
})
export class LedBrightnessComponent implements OnInit {

  constructor(private slaveService: SlaveService) { }

  public brightness = 100;

  ngOnInit(): void {
    this.brightness = this.slaveService.settings['brightness'] * 100;
  }

  formatBrightness(newValue) {
    return newValue + "%";
  }

  onBrightnessChanged(event) {
    this.slaveService.updateBrightness(this.brightness / 100);
  }
}
