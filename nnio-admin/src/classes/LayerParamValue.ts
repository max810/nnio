import NamelessLayerParamValue from '@/classes/NamelessLayerParamValue';

export default class LayerParamValue extends NamelessLayerParamValue {
  constructor(public name: string,
              public type: string,
              public value: any) {
    super(type, value);
  }

  static createDefault() {
    return new LayerParamValue("", "string", "");
  }
}
