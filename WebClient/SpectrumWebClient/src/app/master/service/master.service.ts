import { Injectable } from '@angular/core';
import { Constants } from 'src/app/shared/constants';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MasterService {

  constructor(private httpClient: HttpClient) {}

  public settings;

  private getAllUrl = Constants.API_ADDRESS + "master/getAll";
  private saveAllSettingsUrl = Constants.API_ADDRESS + "saveAllSettings";
  private updateAddress = Constants.API_ADDRESS + "master/update/";
  private updateLowerChunkMarginUrl = this.updateAddress + "lowerChunkMargin";
  private updateHigherChunkMarginUrl = this.updateAddress + "higherChunkMargin";
  private updateDataAmplificationUrl = this.updateAddress + "dataAmplification";
  private updateDataAveragingUrl = this.updateAddress + "dataAveraging"
  private updateAmplitudeClipUrl = this.updateAddress + "amplitudeClip";
  private updateBufferLengthUrl = this.updateAddress + "previousPeaksBufferLength";
  private updateVelocityUrl = this.updateAddress + "velocity";
  private updateMappingStyleUrl = this.updateAddress + "mappingStyle";
  private updateNumberOfBarsUrl = this.updateAddress + "numberOfBars";
  private updateMotorSpeedUrl = this.updateAddress + "motorSpeed";

  private buildParams(value) {
    return { 'newValue': value };
  }

  public getAllSettings() {
    this.httpClient.get(this.getAllUrl).subscribe(result => {
      this.settings = result;
    });
  }

  public isApiAlive() {
    return this.httpClient.get(this.getAllUrl);
  }

  public saveAllSettings() {
    this.httpClient.get(this.saveAllSettingsUrl).toPromise();
  }

  public updateLowerChunkMargin(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateLowerChunkMarginUrl, params, options).subscribe(result => this.getAllSettings());
  }

  public updateHigherChunkMargin(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateHigherChunkMarginUrl, params, options).subscribe(result => this.getAllSettings());
  }

  public updateDataAmplification(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateDataAmplificationUrl, params, options).subscribe(result => this.getAllSettings());
  }

  public updateDataAveraging(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateDataAveragingUrl, params, options).subscribe(result => this.getAllSettings());
  }

  public updateAmplitudeClip(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateAmplitudeClipUrl, params, options).subscribe(result => this.getAllSettings());
  }

  public updateBufferLength(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateBufferLengthUrl, params, options).subscribe(result => this.getAllSettings());
  }

  public updateVelocity(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateVelocityUrl, params, options).subscribe(result => this.getAllSettings());
  }

  public updateMappingStyle(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateMappingStyleUrl, params, options).subscribe(result => this.getAllSettings());
  }

  public updateNumberOfBars(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateNumberOfBarsUrl, params, options).subscribe(result => this.getAllSettings());
  }

  public updateMotorSpeed(newValue) {
    const options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    const params = this.buildParams(newValue);
    this.httpClient.post(this.updateMotorSpeedUrl, params, options).subscribe(result => this.getAllSettings());
  }
}
