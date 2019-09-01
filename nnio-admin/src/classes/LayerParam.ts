import {Dictionary} from 'vue-router/types/router';

export default class LayerParam {
  public isOneOf: boolean;

  static createDefault() {
    return new LayerParam("", "string", false);
  }

  constructor(public name: string,
              public type: string,
              public required: boolean,
              public additionalConstraints: any = {},
              public oneOfs: any[] = []) {
    const defaultConstraints: any = LayerParam.defaultConstraints[this.type];
    if (Object.getOwnPropertyNames(additionalConstraints).length === 0) {
      console.log("EMPTY additionalConstraints");
      this.additionalConstraints = defaultConstraints;
    } else {
      for (let k of Object.keys(defaultConstraints)) {
        if (typeof this.additionalConstraints[k] === "undefined") {
          this.additionalConstraints[k] = defaultConstraints[k];
        }
      }
    }
    this.isOneOf = (oneOfs && oneOfs.length > 0);
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
