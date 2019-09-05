import {Dictionary} from 'vue-router/types/router';
import {JSONDefaults} from '@/constants';

export default class NamelessLayerParamValue {
  public values: Dictionary<any>;

  public get activeValue(): any {
    return this.values[this.type];
  }

  public set activeValue(value) {
    this.values[this.type] = value;
  }

  constructor(public type: string,
              public value: any) {
    this.values = JSON.parse(JSON.stringify(JSONDefaults));
    this.values[type] = value;
  }
}
