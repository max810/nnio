<template xmlns:v-model="http://www.w3.org/1999/xhtml">
  <div class="container">
    <div class="row">
      <div class="col-4">
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
      <div class="col-8">
        <div class="tab-content" id="nav-tabContent">
          <!--TODO: add additional constraints: https://getbootstrap.com/docs/4.3/components/collapse/#example
          TODO filter like this https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_js_dropdown_filter-->

          <div
              v-for="lSchema of layerSchemas"
              v-bind:key="lSchema.layerType"
              class="tab-pane fade show"
              v-bind:id="`list-${lSchema.layerType}`"
              role="tabpanel"
              v-bind:aria-labelledby="`list-${lSchema.layerType}-list`"
          >
            PARAMETERS
            <table class="table">
              <tr v-for="prop of lSchema.layerParams"
                  v-bind:key="prop.name">
                <td>
                  <label v-bind:for="`${lSchema.layerType}-${prop.name}-type-select`">
                    <input type="text"
                           v-model:value="prop.name">
                  </label>
                </td>
                <td>
                  <div class="form-check form-check-inline">
                    <select v-model="prop.type"
                            v-bind:id="`${lSchema.layerType }-${prop.name}-type-select`"
                            class="selectpicker form-check-input">
                      <option v-for="t of jsonTypes">
                        {{ t }}
                      </option>
                    </select>
                    <label class="form-check-label">
                      <input type="checkbox" v-model="prop.required">
                      Required
                    </label>
                  </div>
                  <div>
                    <a
                        class
                        data-toggle="collapse"
                        v-bind:href="`#${lSchema.layerType}-${prop.name}-additional-constraints`"
                        role="button"
                        aria-expanded="false"
                        aria-controls="collapseExample">
                      Additional constraints
                    </a>
                    <div
                        class="collapse"
                        v-bind:id="`${lSchema.layerType}-${prop.name}-additional-constraints`">
                      <div class="card card-body">TODO ;)
                        <div>{{ }}</div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </table>
            <!--            {# {{ layer_schema['properties'].keys() }}#}-->
            <!--            {# TODO - add content (fields, types, "edit" buttons), etc. #}-->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import {Component, Vue} from "vue-property-decorator";
  import {Dictionary} from "vue-router/types/router";
  import Axios from "axios";
  import {backendUrls} from "@/constants";

  @Component({})
  export default class Admin extends Vue {
    layerSchemas: LayerSchema[] = [];
    jsonTypes = ['string', 'integer', 'number', 'array', 'boolean', 'object'];

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
          return LayerParam.getDefaultConstraints(type_);
        case "number":
        case "integer":
          return {
            maximum: prop.maximum || null,
            minimum: prop.minimum || null,
          };
        case "array":
          const items = prop.items;
          // items will NEVER be Array, only object
          return {
            maxItems: items.maxItems || null,
            minItems: items.minItems || null,
            itemsType: items.type || null,
          };
        case "object":
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
        .then(response => {
          console.log(response);
          this.layerSchemas = Admin.parseLayersSchemas(response.data);
        });

      console.log(this.layerSchemas);
    }
  }

  class LayerParam {
    constructor(public name: string,
                public type: string,
                public required: boolean,
                public additionalConstraints: any = {}) {
      if (!additionalConstraints) {
        this.additionalConstraints = LayerParam.getDefaultConstraints(this.type);
      }
    }

    //
    // generateConstraintsTemplates() {
    //   // TODO
    //   switch (this.type) {
    //     case "array":
    //       return `<input type="number" v-model="this.">`;
    //     default:
    //       throw new Error(`Invalid type ${this.type}!`);
    //   }
    // }

    static getDefaultConstraints(type_: string) {
      //TODO : think about oneOf (enum)
      switch (type_) {
        case "number":
        case "integer":
          return {
            maximum: null,
            minimum: null,
          };
        case "array":
          return {
            minItems: null,
            maxItems: null,
            itemsType: null,
          };
        case "boolean":
        case "string":
        case "object":
        default:
          return {};
      }
    }
  }

  class LayerSchema {
    constructor(public layerType: string, public layerParams: LayerParam[]) {
    }
  }
</script>

<style scoped>
</style>