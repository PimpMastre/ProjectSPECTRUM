import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-motor-speed',
  templateUrl: './motor-speed.component.html',
  styleUrls: ['./motor-speed.component.scss']
})
export class MotorSpeedComponent implements OnInit {

  constructor() { }

  public motorSpeed = 1000;

  ngOnInit(): void {
  }

  formatMotorSpeed(newValue) {
    if(newValue < 1020) {
      return 'Off';
    }
    
    return newValue;
  }

  onMotorSpeedChanged(event) {

  }
}
