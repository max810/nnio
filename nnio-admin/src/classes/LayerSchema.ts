import LayerParam from '@/classes/LayerParam';

export default class LayerSchema {
  constructor(public layerType: string, public layerParams: LayerParam[]) {
  }
}