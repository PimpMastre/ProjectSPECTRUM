import { Component, OnInit } from '@angular/core';
import { MasterService } from '../../service/master.service';

@Component({
  selector: 'app-amplitude-settings',
  templateUrl: './amplitude-settings.component.html',
  styleUrls: ['./amplitude-settings.component.scss']
})
export class AmplitudeSettingsComponent implements OnInit {

  constructor(private masterService: MasterService) { }

  public amplitudeClip = 1000000;
  public dataAmplification = 0;

  ngOnInit(): void {
    this.amplitudeClip = this.masterService.settings['amplitudeClip'];
    this.dataAmplification = this.masterService.settings['dataAmplification'];
  }

  formatAmplitudeClip(value) {
    return (value / 1000000).toFixed(2) + 'M';
  }

  formatDataAmplification(value) {
    return value + "%";
  }

  onDataAmplificationChanged(event) {
    this.dataAmplification = event.value;

    this.masterService.updateDataAmplification(this.dataAmplification);
  }

  onAmplitudeClipChanged(event) {
    this.amplitudeClip = event.value;
    this.amplitudeClip = Math.floor(this.amplitudeClip / 1000) * 1000;

    this.masterService.updateAmplitudeClip(this.amplitudeClip);
  }
}
