import { Component, OnInit } from '@angular/core';
import { MasterService } from '../../service/master.service';

@Component({
  selector: 'app-mapping-styles',
  templateUrl: './mapping-styles.component.html',
  styleUrls: ['./mapping-styles.component.scss']
})
export class MappingStylesComponent implements OnInit {

  constructor(private masterService: MasterService) { }
  public mappingStyles = ['Linear Space', 'Geometric Space']
  public selectedMappingStyle = this.mappingStyles[0];

  ngOnInit(): void {
    this.selectedMappingStyle = this.mappingStyles[this.masterService.settings['mappingStyle']];
  }

  onStyleChanged(event) {
    var styleValue;
    if(this.selectedMappingStyle == this.mappingStyles[0]) {
      styleValue = 0;
    }
    else {
      styleValue = 1;
    }

    this.masterService.updateMappingStyle(styleValue);
  }

}
