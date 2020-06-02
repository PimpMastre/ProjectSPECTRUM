import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatOptionModule } from '@angular/material/core';
import { MatSelectModule } from '@angular/material/select';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MasterComponent } from './master/master.component';
import { SlaveComponent } from './slave/slave.component';
import { MatTabsModule } from '@angular/material/tabs';
import { NumberOfBarsComponent } from './master/sub-components/number-of-bars/number-of-bars.component';
import { ChunkMarginsComponent } from './master/sub-components/chunk-margins/chunk-margins.component';
import { AmplitudeSettingsComponent } from './master/sub-components/amplitude-settings/amplitude-settings.component';
import { MappingStylesComponent } from './master/sub-components/mapping-styles/mapping-styles.component';
import { BuffersComponent } from './master/sub-components/buffers/buffers.component';
import { MotorSpeedComponent } from './master/sub-components/motor-speed/motor-speed.component';
import { ColorSettingsComponent } from './slave/sub-components/color-settings/color-settings.component';
import { LedFalloffComponent } from './slave/sub-components/led-falloff/led-falloff.component';
import { MatSliderModule } from '@angular/material/slider';

@NgModule({
  declarations: [
    AppComponent,
    MasterComponent,
    SlaveComponent,
    NumberOfBarsComponent,
    ChunkMarginsComponent,
    AmplitudeSettingsComponent,
    MappingStylesComponent,
    BuffersComponent,
    MotorSpeedComponent,
    ColorSettingsComponent,
    LedFalloffComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSidenavModule,
    MatOptionModule,
    MatSelectModule,
    MatListModule,
    MatIconModule,
    MatToolbarModule,
    MatButtonModule,
    MatTabsModule,
    MatSliderModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
