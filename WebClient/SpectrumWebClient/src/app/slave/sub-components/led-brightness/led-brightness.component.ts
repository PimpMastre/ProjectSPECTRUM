import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-led-brightness',
  templateUrl: './led-brightness.component.html',
  styleUrls: ['./led-brightness.component.scss']
})
export class LedBrightnessComponent implements OnInit {

  constructor() { }

  public brightness = 100;

  ngOnInit(): void {
  }

  formatBrightness(newValue) {
    return newValue + "%";
  }

  onBrightnessChanged(event) {
    console.log(event);
  }
}
