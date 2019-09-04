<template>
  <div class="container">
    <div class="row">
      <div class="col-2">
        <div class="list-group" id="list-tab" role="tablist">
          <a
              v-for="lSchema of layerSchemas"
              v-bind:key="lSchema.layerType"
              class="list-group-item list-group-item-action"
              v-bind:id="`list-${lSchema.layerType}-list`"
              data-toggle="list"
              v-bind:href="`#list-${lSchema.layerType}`"
              role="tab"
              v-bind:aria-controls="lSchema.layerType"
          >{{ lSchema.layerType }}</a>
        </div>
      </div>
      <div class="col-10">
        <div class="tab-content" id="nav-tabContent">
          <div
              v-for="lSchema of layerSchemas"
              class="tab-pane fade show"
              v-bind:id="`list-${lSchema.layerType}`"
              role="tabpanel"
              v-bind:aria-labelledby="`list-${lSchema.layerType}-list`"
          >
            <!--        for div ^      v-bind:key="lSchema.layerType"-->
            <params-list v-bind:params="lSchema.layerParams" v-bind:baseId="lSchema.layerType">
            </params-list>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<!--
TODO:
  add `type` <select> to ParamsValuesList (it is parsed correctly, but you can't add Object props to Objects)
  add `rename layer` functionality
 -->
<div>

</div>
<script lang="ts">
  import VRuntimeTemplate from "v-runtime-template";
  import {Component, Vue} from "vue-property-decorator";
  import {Dictionary} from "vue-router/types/router";
  import Axios from "axios";
  import {backendUrls, JSONTypes} from "@/constants";
  import LayerSchema from '@/classes/LayerSchema';
  import LayerParam from '@/classes/LayerParam';
  import Constraints from '@/components/Constraints.vue';
  import ParamsList from '@/components/ParamsList.vue';
  import LayerParamValue from '@/classes/LayerParamValue';

  @Component({
    components: {ParamsList, Constraints, VRuntimeTemplate}
  })
  export default class Admin extends Vue {
    layerSchemas: LayerSchema[] = [];
    JSONTypes = JSONTypes;

    static parseLayersSchemas(json: string | object) {
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
          const lp = Admin.parseLayerParam(pName, pValue as any, requiredParams);
          layerParams.push(lp);
        }
        const layerSchema = new LayerSchema(layerType, layerParams);

        results.push(layerSchema);
      }
      (<any>window).SCHEMA = results;
      return results;
    }

    static parseOneOfs(prop: any, type: string) {
      const oneOfs: any[] = prop.enum || [];
      if (type !== 'object' && type !== 'array') {
        return oneOfs.map(val => new LayerParamValue("", type, val));
      } else {
        const res: LayerParamValue[][] = [];
        for (const example of oneOfs) {
          const exampleParams: LayerParamValue[] = [];
          for (const [pName, pValue] of Object.entries(example)) {
            exampleParams.push(this.parseLayerParamValues(pValue, pName));
          }
          res.push(exampleParams);
        }
        return res;
      }
    }

    static parseLayerParam(pName: string, pValue: any, requiredParams: string[]) {
      let paramValue_ = pValue as any;
      const name_ = pName;
      const type_ = paramValue_["type"];
      const required_ = requiredParams.includes(name_);
      const oneOfs = Admin.parseOneOfs(paramValue_, type_);

      const constraints_ =
        (oneOfs && oneOfs.length > 0)
          ? LayerParam.defaultConstraints[type_]
          : Admin.parseConstraints(paramValue_);

      return new LayerParam(name_, type_, required_, constraints_, oneOfs);
    }

    static parseLayerParamValues(prop: any, pName: string) {
      const pType = Array.isArray(prop) ? "array" : typeof prop;
      let value = prop;
      if (pType === 'object' || pType === 'array') {
        const res: LayerParamValue[] = [];
        for (const [pName_1, pValue_1] of Object.entries(prop)) {
          res.push(this.parseLayerParamValues(pValue_1, pName_1));
        }
        value = res;
      }

      return new LayerParamValue(pName, pType, value);
    }

    static parseConstraints(prop: any, type_: string = prop.type) {
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
          // items will NEVER be Array, only object
          return {
            maxItems: typeof items.maxItems === "undefined" ? null : items.maxItems,
            minItems: typeof items.minItems === "undefined" ? null : items.minItems,
            itemsType: typeof items.type === "undefined" ? null : items.type,
          };
        case "object":
          let res: any = [];
          for (const k of Object.keys(prop.properties)) {
            const localProp = prop.properties[k];
            res.push(this.parseLayerParam(k, localProp, prop.required));
          }

          res = {'paramsConstraints': res};

          return res;
      }
    }

    mounted() {
      console.log("MOUNTED!");
      Axios
        .get(backendUrls.getLayersSchemas)
        .then(
          response => {
            console.log(response);
            this.layerSchemas = Admin.parseLayersSchemas(response.data);
          },
          err => {
            if (err.status == 401) {
              this.$router.push({name: 'login', params: {msg: 'LOGIN EXPIRED'}});
            }
          });

      console.log(this.layerSchemas);
    }
  }

</script>

<style>

</style>