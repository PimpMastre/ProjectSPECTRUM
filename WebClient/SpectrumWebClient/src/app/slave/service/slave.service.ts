import { Injectable } from '@angular/core';
import { Constants } from 'src/app/shared/constants';
import { HttpHeaders, HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SlaveService {
  constructor(private httpClient: HttpClient) { }

  public settings;

  private getAllAddress = Constants.API_ADDRESS + "slave/getAll";
  private updateAddress = Constants.API_ADDRESS + "slave/update/";
  private updateLedFalloffUrl = this.updateAddress + "ledFalloff";
  private updateBrightnessUrl = this.updateAddress + "brightness";
  private updateColorsUrl = this.updateAddress + "colors/";

  public getAllSettings() {
    this.httpClient.get(this.getAllAddress).subscribe(result => {
      this.settings = result;
    });
  }

  private buildParams(value) {
    return { 'newValue': value };
  }

  private buildColorParams(rgba) {
    return { 'newValue': [rgba.r, rgba.g, rgba.b] };
  }

  public updateLedFalloff(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateLedFalloffUrl, params, options);
  }

  public updateBrightness(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateBrightnessUrl, params, options);
  }

  public updateColors(index, newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildColorParams(newValue);
    this.httpClient.post(this.updateColorsUrl + index, params, options);
  }
}
