import {Dictionary} from 'vue-router/types/router';
import LayerSchema from '@/classes/LayerSchema';
import LayerParam from '@/classes/LayerParam';
import LayerParamValue from '@/classes/LayerParamValue';

export function parseLayersSchemas(json: string | object) {
  let data: Dictionary<any>;
  let results: Array<LayerSchema> = [];
  if (typeof json == "string") {
    data = JSON.parse(json) as Dictionary<any>;
  } else {
    data = json as Dictionary<any>;
  }

  for (const [layerType, layerData] of Object.entries(data)) {
    const params = layerData.properties.params.properties || {};
    const requiredParams: string[] = layerData.properties.params.required;
    const layerParams: LayerParam[] = [];

    for (const [pName, pValue] of Object.entries(params)) {
      const lp = parseLayerParam(pName, pValue as any, requiredParams);
      layerParams.push(lp);
    }
    const layerSchema = new LayerSchema(layerType, layerParams);

    results.push(layerSchema);
  }
  (<any>window).SCHEMA = results;
  return results;
}

function parseOneOfs(prop: any, type: string) {
  const oneOfs: any[] = prop.enum || [];
  if (type !== 'object' && type !== 'array') {
    return oneOfs.map(val => new LayerParamValue("", type, val));
  } else {
    const res: LayerParamValue[][] = [];
    for (const example of oneOfs) {
      const exampleParams: LayerParamValue[] = [];
      for (const [pName, pValue] of Object.entries(example)) {
        exampleParams.push(parseLayerParamValues(pValue, pName));
      }
      res.push(exampleParams);
    }
    return res;
  }
}

function parseLayerParam(pName: string, pValue: any, requiredParams: string[]) {
  let paramValue_ = pValue as any;
  const name_ = pName;
  const type_ = paramValue_["type"];
  const required_ = (requiredParams || []).includes(name_);
  const oneOfs = parseOneOfs(paramValue_, type_);

  const constraints_ =
    (oneOfs && oneOfs.length > 0)
      ? LayerParam.defaultConstraints[type_]
      : parseConstraints(paramValue_);

  return new LayerParam(name_, type_, required_, constraints_, oneOfs);
}

function parseLayerParamValues(prop: any, pName: string) {
  const pType = Array.isArray(prop) ? "array" : typeof prop;
  let value = prop;
  if (pType === 'object' || pType === 'array') {
    const res: LayerParamValue[] = [];
    for (const [pName_1, pValue_1] of Object.entries(prop)) {
      res.push(parseLayerParamValues(pValue_1, pName_1));
    }
    value = res;
  }

  return new LayerParamValue(pName, pType, value);
}

function parseConstraints(prop: any, type_: string = prop.type): any {
  switch (type_) {
    case "string":
    case "boolean":
      return LayerParam.defaultConstraints[type_];
    case "number":
    case "integer":
      return {
        maximum: typeof prop.maximum === "undefined" ? null : prop.maximum,
        minimum: typeof prop.minimum === "undefined" ? null : prop.minimum,
      };
    case "array":
      const items = prop.items || {};
      // items mustn't EVER be Array, only object
      return {
        maxItems: typeof prop.maxItems === "undefined" ? null : prop.maxItems,
        minItems: typeof prop.minItems === "undefined" ? null : prop.minItems,
        itemsConstraints: parseLayerParam("itemsConstraints", items, ["itemsConstraints"])
      };
    case "object":
      let res: any = [];
      for (const k of Object.keys(prop.properties)) {
        const localProp = prop.properties[k];
        res.push(parseLayerParam(k, localProp, prop.required));
      }

      return res;
  }
}
