import { Component, OnInit } from '@angular/core';
import { style, trigger, transition, animate } from '@angular/animations';
import { HttpClient } from '@angular/common/http';
import { MasterService } from './master/service/master.service';
import { SlaveService } from './slave/service/slave.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
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
            animate('1s ease-in', 
                    style({ opacity: 0 }))
          ]
        )
      ]
    )
  ]
})
export class AppComponent implements OnInit{
  isExpanded = true;
  isShowing = false;

  isConnecting = true;
  connectionError = false;

  constructor(private masterService: MasterService, private slaveService: SlaveService) {

  }
  ngOnInit(): void {
    this.masterService.isApiAlive().subscribe(result => {
      this.isConnecting = false;
      this.connectionError = false;

      this.masterService.getAllSettings();
      this.slaveService.getAllSettings();
    },
    error => {
      this.isConnecting = true;
      this.connectionError = true;
    })
  }

  mouseenter() {
    if (!this.isExpanded) {
      this.isShowing = true;
    }
  }

  mouseleave() {
    if (!this.isExpanded) {
      this.isShowing = false;
    }
  }

  saveAllSettingsClicked($event) {
    this.masterService.saveAllSettings();
  }
}
