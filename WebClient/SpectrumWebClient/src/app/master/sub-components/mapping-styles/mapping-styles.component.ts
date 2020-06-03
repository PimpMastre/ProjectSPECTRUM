import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-mapping-styles',
  templateUrl: './mapping-styles.component.html',
  styleUrls: ['./mapping-styles.component.scss']
})
export class MappingStylesComponent implements OnInit {

  constructor() { }
  public mappingStyles = ['Linear Space', 'Geometric Space']
  public selectedMappingStyle = this.mappingStyles[0];

  ngOnInit(): void {
  }

  onStyleChanged(event) {
    
  }

}
