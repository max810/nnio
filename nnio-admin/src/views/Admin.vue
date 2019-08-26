<template xmlns:v-model="http://www.w3.org/1999/xhtml">
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
          <!--TODO: add additional constraints: https://getbootstrap.com/docs/4.3/components/collapse/#example
          TODO filter like this https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_js_dropdown_filter-->

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
    testMsg: string = "1234";
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
      delete paramValue_["type"];
      const required_ = requiredParams.includes(name_);
      const constraints_ = Admin.parseConstraints(paramValue_, type_);

      return new LayerParam(name_, type_, required_, constraints_);
    }


    static parseConstraints(prop: any, type_: string) {
      switch (type_) {
        case "string":
        case "boolean":
          // TODO - think about oneOf (enum)
          return LayerParam.defaultConstraints[type_];
        case "number":
        case "integer":
          return {
            maximum: prop.maximum || null,
            minimum: prop.minimum || null,
          };
        case "array":
          const items = prop.items || {};
          // items will NEVER be Array, only object
          return {
            maxItems: items.maxItems || null,
            minItems: items.minItems || null,
            itemsType: items.type || null,
          };
        case "object":
          return {};
        // TODO
        // const propParams: LayerParam[] = [];
        // for (const [pName, pValue] of Object.entries(prop.properties)) {
        //   const pp = Admin.parseLayerParam(pName, pValue as any, prop.required || []);
        //   propParams.push(pp);
        // }
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