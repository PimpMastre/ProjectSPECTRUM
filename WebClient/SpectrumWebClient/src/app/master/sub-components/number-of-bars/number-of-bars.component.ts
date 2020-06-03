import { Component, OnInit } from '@angular/core';
import { MasterService } from '../../service/master.service';

@Component({
  selector: 'app-number-of-bars',
  templateUrl: './number-of-bars.component.html',
  styleUrls: ['./number-of-bars.component.scss']
})
export class NumberOfBarsComponent implements OnInit {

  constructor(private masterService: MasterService) { }

  public numberOfBars = 5;

  ngOnInit(): void {
    this.numberOfBars = this.masterService.settings['numberOfBars'];
  }

  onNumberOfBarsChanged(event) {
    if(event.target.value < 1) {
      this.numberOfBars = 0;
    }

    this.masterService.updateNumberOfBars(this.numberOfBars);
  }
}
