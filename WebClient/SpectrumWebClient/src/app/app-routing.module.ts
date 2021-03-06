import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MasterComponent } from './master/master.component';
import { SlaveComponent } from './slave/slave.component';
import { MotorSpeedComponent } from './master/sub-components/motor-speed/motor-speed.component';


const routes: Routes = [
  { path: 'master', component: MasterComponent },
  { path: 'slave', component: SlaveComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
