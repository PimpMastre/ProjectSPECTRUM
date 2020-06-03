import { Component, OnInit } from '@angular/core';
import { MasterService } from '../../service/master.service';

@Component({
  selector: 'app-motor-speed',
  templateUrl: './motor-speed.component.html',
  styleUrls: ['./motor-speed.component.scss']
})
export class MotorSpeedComponent implements OnInit {

  constructor(private masterService: MasterService) { }

  public motorSpeed = 1000;

  ngOnInit(): void {
    this.motorSpeed = this.masterService.settings['motorSpeed'];
  }

  formatMotorSpeed(newValue) {
    if(newValue < 1020) {
      return 'Off';
    }
    
    return newValue;
  }

  onMotorSpeedChanged(event) {
    this.masterService.updateMotorSpeed(this.motorSpeed);
  }
}
