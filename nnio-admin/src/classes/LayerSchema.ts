import LayerParam from '@/classes/LayerParam';

export default class LayerSchema {
  constructor(public layerType: string, public layerParams: LayerParam[]) {
  }

  static createDefault() {
    return new LayerSchema("NewLayer", []);
  }
}