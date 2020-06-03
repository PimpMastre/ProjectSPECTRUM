import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-amplitude-settings',
  templateUrl: './amplitude-settings.component.html',
  styleUrls: ['./amplitude-settings.component.scss']
})
export class AmplitudeSettingsComponent implements OnInit {

  constructor() { }

  public amplitude = 1000000;

  ngOnInit(): void {
  }

  formatAmplitude(value) {
    return (value / 1000000).toFixed(2) + 'M';
  }

  onAmplitudeChanged(event) {
    this.amplitude = event.value;
    this.amplitude = Math.floor(this.amplitude / 1000) * 1000;
  }
}
