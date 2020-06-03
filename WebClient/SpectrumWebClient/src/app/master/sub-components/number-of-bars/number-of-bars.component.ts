import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-number-of-bars',
  templateUrl: './number-of-bars.component.html',
  styleUrls: ['./number-of-bars.component.scss']
})
export class NumberOfBarsComponent implements OnInit {

  constructor() { }

  public numberOfBars = 5;

  ngOnInit(): void {
  }

  onNumberOfBarsChanged(event) {
    if(event.target.value < 1) {
      this.numberOfBars = 0;
    }
  }
}
