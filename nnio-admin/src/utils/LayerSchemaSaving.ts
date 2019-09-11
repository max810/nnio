import LayerSchema from '@/classes/LayerSchema';
import LayerParam from '@/classes/LayerParam';
import NamelessLayerParamValue from '@/classes/NamelessLayerParamValue';
import LayerParamValue from '@/classes/LayerParamValue';

export function layerSchemasToJsonSchemas(schemas: LayerSchema[]): any {
  const allSchemas: any = {};
  for (const s of schemas) {
    const props: any = {};
    const required: Array<string> = [];
    for (const lp of s.layerParams) {
      props[lp.name] = convertLayerParam(lp);
      if (lp.required) {
        required.push(lp.name);
      }
    }

    allSchemas[s.layerType] = {
      $schema: "http://json-schema.org/draft-04/schema#",
      type: "object",
      properties: {
        name: {
          type: "string"
        },
        type: {
          type: "string"
        },
        inputs: {
          type: "array",
          items: {
            type: "string"
          }
        },
        params: {
          type: "object",
          properties: props,
          required: required,
        },
        required: [
          "name",
          "type",
          "inputs",
          "params"
        ]
      }
    };
  }

  return allSchemas;
}


function convertLayerParam(layerParam: LayerParam) {
  const res: any = {
    type: layerParam.type,
  };
  if (!layerParam.isOneOf) {
    if (!['array', 'object'].includes(layerParam.type)) {
      for (const [k, v] of Object.entries(layerParam.activeConstraints)) {
        if (v !== null)
          res[k] = v;
      }
    } else if (layerParam.type == 'array') {
      for (const [k, v] of Object.entries(layerParam.activeConstraints)) {
        if (k !== 'itemsConstraints' && v !== null) {
          res[k] = v;
        }
      }
      res['items'] = convertLayerParam(layerParam.activeConstraints.itemsConstraints);
    } else { // object
      res['properties'] = {};
      for (const layerParamInner of layerParam.activeConstraints) {
        res['properties'][layerParamInner.name] = convertLayerParam(layerParamInner);
      }
      res['required'] = (<LayerParam[]>layerParam.activeConstraints)
        .filter(x => x.required)
        .map(x => x.name);
    }
  } else {
    if (layerParam.type === 'array') {
      res['enum'] = (layerParam.activeOneOfs as NamelessLayerParamValue[][]).map((x: any) => x.map((y: any) => convertLayerParamValue(y)));
    } else if (layerParam.type === 'object') {
      res['enum'] = [];
      for (const lpvArr of layerParam.activeOneOfs as NamelessLayerParamValue[][]) {
        const obj: any = {};
        for (const lpv of lpvArr) {
          obj[(lpv as LayerParamValue).name] = convertLayerParamValue(lpv);
        }
        res['enum'].push(obj);
      }
    } else {
      res['enum'] = (layerParam.activeOneOfs as NamelessLayerParamValue[]).map(x => convertLayerParamValue(x));
    }

  }

  return res;
}

function convertLayerParamValue(
  layerParamValue: NamelessLayerParamValue)
  : any {
  if (layerParamValue.type === 'object') {
    const res: any = {};
    for (const lpv of layerParamValue.activeValue) {
      res[lpv.name] = convertLayerParamValue(lpv);
    }
    return res;
  } else if (layerParamValue.type === 'array') {
    return (layerParamValue.activeValue)
      .map((x: any) => convertLayerParamValue(x));
  } else {
    return (layerParamValue as NamelessLayerParamValue).activeValue;
  }
}