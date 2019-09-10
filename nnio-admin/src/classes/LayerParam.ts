import {Dictionary} from 'vue-router/types/router';
import {JSONTypes} from '@/constants';
import NamelessLayerParamValue from '@/classes/NamelessLayerParamValue';

export default class LayerParam {
  public isOneOf: boolean;
  public additionalConstraints: any = JSON.parse(JSON.stringify(LayerParam.defaultConstraints)); // basically a copy
  public oneOfs: Dictionary<NamelessLayerParamValue[] | NamelessLayerParamValue[][]>;

  public get activeOneOfs(): NamelessLayerParamValue[] | NamelessLayerParamValue[][] {
    return this.oneOfs[this.type];
  }

  public get activeConstraints(): LayerParam[] | any {
    return this.additionalConstraints[this.type];
  }

  constructor(public name: string,
              public type: string,
              public required: boolean,
              constraints: Dictionary<LayerParam[] | any> = {},
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
        itemsConstraints: []
      },
    boolean: {},
    string: {},
    object: [],
  };
}
