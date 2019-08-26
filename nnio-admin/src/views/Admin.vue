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
            <params-list v-bind:params="lSchema.layerParams" v-bind:collapseBaseId="lSchema.layerType">
            </params-list>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<!--
TODO:
  Add constraints for array elements (like object),
  add `add` and `delete` functionality for properties and constraints,
  add `oneOf` (enum) functionality to constraints
  add `save` functionality
 -->
<div>

</div>
<!--
FIXME:
  fix undefined in baseId
-->
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

      console.log({results});

      return results;
    }

    static parseLayerParam(pName: string, pValue: string, requiredParams: string[]) {
      let paramValue_ = pValue as any;
      const name_ = pName;
      const type_ = paramValue_["type"];
      const required_ = requiredParams.includes(name_);
      const constraints_ = Admin.parseConstraints(paramValue_);

      return new LayerParam(name_, type_, required_, constraints_);
    }

    static parseConstraints(prop: any, type_: string = prop.type) {
      console.log(`PARSING`);
      console.log(prop);
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
          console.log("OBJECT");
          let res: any = [];
          for (const k of Object.keys(prop.properties)) {
            const localProp = prop.properties[k];
            res.push(this.parseLayerParam(k, localProp, prop.required));
          }
          (window as any).RES = res;
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