import {Dictionary} from 'vue-router/types/router';

export default class LayerParam {
  constructor(public name: string,
              public type: string,
              public required: boolean,
              public additionalConstraints: any = {}) {
    const defaultConstraints: any = LayerParam.defaultConstraints[this.type];
    if (!additionalConstraints) {
      this.additionalConstraints = defaultConstraints;
    } else {
      for (let k of Object.keys(defaultConstraints)) {
        if (typeof this.additionalConstraints[k] === "undefined") {
          this.additionalConstraints[k] = defaultConstraints[k];
        }
      }
    }
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
    object: {},
  };
}
