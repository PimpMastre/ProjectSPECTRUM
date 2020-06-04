import { Component, OnInit, ViewChild } from '@angular/core';
import { ChartOptions, ChartType } from 'chart.js';
import { Label, SingleDataSet, BaseChartDirective } from 'ng2-charts';
import { trigger, transition, style, animate } from '@angular/animations';
import { SlaveService } from '../../service/slave.service';
import { MasterService } from 'src/app/master/service/master.service';

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

  constructor(private slaveService: SlaveService, private masterService: MasterService) { }

  @ViewChild(BaseChartDirective)
  public chart: BaseChartDirective;

  public pieChartOptions: ChartOptions = {
    responsive: true,
    tooltips: {
      enabled: false
    }
  };
  public pieChartData: SingleDataSet = [];
  public pieChartColors: Array<any> = [{backgroundColor: []}];
  public pieChartType: ChartType = 'pie';

  public activeSection = null;
  public currentColor;

  ngOnInit(): void {
    var numberOfBars = this.masterService.settings['numberOfBars'];
    var colors = this.slaveService.settings['colors'].split(",");
    for(var i = 0; i < numberOfBars; ++i) {
      this.pieChartData.push(1);
      this.pieChartColors[0].backgroundColor.push(this.rgbToHex([colors[3 * i], colors[3 * i + 1], colors[3 * i + 2]]));
    }
  }

  private rgbToHex(rgb) {
      var rez = rgb[2] | (rgb[1] << 8) | (rgb[0] << 16);
      return '#' + (0x1000000 + rez).toString(16).slice(1)
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
    for(var i = 0; i < this.masterService.settings['numberOfBars']; ++i) {
      if(i != this.activeSection) {
        newChartData.push(1)
      }
      else {
        newChartData.push(this.masterService.settings['numberOfBars'] - 1);
      }
    }
    this.pieChartData = newChartData;
    this.chart.chart.update();
  }

  colorChangeComplete(event) {
    this.pieChartColors[0].backgroundColor[this.activeSection] = event.color.hex;
    this.chart.chart.update();
    
    this.slaveService.updateColors(this.activeSection, event.color.rgb);
  }
}
