import {Dictionary} from 'vue-router/types/router';
import {JSONTypes} from '@/constants';

export default class LayerParam {
  public isOneOf: boolean;
  public additionalConstraints: any = JSON.parse(JSON.stringify(LayerParam.defaultConstraints)); // basically a copy
  public oneOfs: Dictionary<any[]>;

  public get activeOneOfs(): any[] {
    return this.oneOfs[this.type];
  }

  public get activeConstraints(): any {
    return this.additionalConstraints[this.type];
  }

  constructor(public name: string,
              public type: string,
              public required: boolean,
              constraints: Dictionary<any> = {},
              oneOfs: any[] = []) {
    this.oneOfs = {};
    for (const k of JSONTypes) {
      this.oneOfs[k] = [];
    }
    this.oneOfs[type] = oneOfs || [];
    this.additionalConstraints[type] = constraints || LayerParam.defaultConstraints[type];
    this.isOneOf = (oneOfs && oneOfs.length > 0);
  }

  static createDefault() {
    return new LayerParam("", "string", false);
  }

  static readonly defaultConstraints: Dictionary<object> = {
    number:
      {
        maximum: null,
        minimum: null,
      },
    integer:
      {
        maximum: null,
        minimum: null,
      },
    array:
      {
        minItems: null,
        maxItems: null,
        itemsType: null,
      },
    boolean: {},
    string: {},
    object: {'paramsConstraints': []},
  };
}
