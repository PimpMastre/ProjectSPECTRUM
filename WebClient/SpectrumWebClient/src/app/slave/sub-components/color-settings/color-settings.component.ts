import { Component, OnInit, ViewChild } from '@angular/core';
import { ChartOptions, ChartType } from 'chart.js';
import { Label, SingleDataSet, BaseChartDirective } from 'ng2-charts';
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-color-settings',
  templateUrl: './color-settings.component.html',
  styleUrls: ['./color-settings.component.scss'],
  animations: [
    trigger(
      'inOutAnimation', 
      [
        transition(
          ':enter', 
          [
            style({ opacity: 0 }),
            animate('0.5s ease-out', 
                    style({ opacity: 1 }))
          ]
        ),
        transition(
          ':leave', 
          [
            style({ opacity: 1 }),
            animate('0.5s ease-in', 
                    style({ opacity: 0 }))
          ]
        )
      ]
    )
  ]
})
export class ColorSettingsComponent implements OnInit {

  constructor() { }

  @ViewChild(BaseChartDirective)
  public chart: BaseChartDirective;

  public pieChartOptions: ChartOptions = {
    responsive: true,
    tooltips: {
      enabled: false
    }
  };
  public pieChartLabels: Label[] = []
  public pieChartData: SingleDataSet = [];
  public pieChartColors: Array<any> = [{backgroundColor: []}];
  public pieChartType: ChartType = 'pie';

  public activeSection = null;
  public currentColor;

  ngOnInit(): void {
    var total = 5;
    for(var i = 0; i < total; ++i) {
      this.pieChartLabels.push("Section " + i);
      this.pieChartData.push(1);
      this.pieChartColors[0].backgroundColor.push('#000000');
    }
  }

  onSectionClicked(event) {
    if(event.active.length > 0) {
      var newValue = event.active[0]._index;
    }
    else {
      newValue = this.activeSection;
    }

    if(this.activeSection == newValue) {
      this.activeSection = null;
    }
    else {
      this.activeSection = event.active[0]._index;
      this.currentColor = this.pieChartColors[0].backgroundColor[this.activeSection];
    }
  
    this.highlightChartSection();
  }

  highlightChartSection() {
    var newChartData: SingleDataSet = [];
    for(var i = 0; i < 5; ++i) {
      if(i != this.activeSection) {
        newChartData.push(1)
      }
      else {
        newChartData.push(4);
      }
    }
    this.pieChartData = newChartData;
    this.chart.chart.update();
  }

  changeComplete(event) {
    this.pieChartColors[0].backgroundColor[this.activeSection] = event.color.hex;
    this.chart.chart.update();
  }
}
