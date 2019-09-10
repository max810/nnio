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
          <div class="list-group-item">
            <button class="btn btn-primary" v-on:click="addLayerSchema" style="width: 100%; height: 100%;">+
            </button>
          </div>
          <br>
          <br>
          <br>
          <br>
          <div class="list-group-item">
            <button class="btn btn-success" v-on:click="saveSchemas" style="width: 100%; height: 100%;">Save
            </button>
          </div>
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
            Rename layer: <input v-model="lSchema.layerType">
            <close-button v-on:click="deleteLayerSchema(param)"></close-button>
            <br>
            <br>
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
  add save functionality
 -->
<div>

</div>
<script lang="ts">
  import VRuntimeTemplate from "v-runtime-template";
  import {Component, Vue} from "vue-property-decorator";
  import Axios from "axios";
  import {backendUrls, JSONTypes} from "@/constants";
  import LayerSchema from '@/classes/LayerSchema';
  import Constraints from '@/components/Constraints.vue';
  import ParamsList from '@/components/ParamsList.vue';
  import CloseButton from '@/components/CloseButton.vue';
  import {parseLayersSchemas} from '@/utils/LayerSchemaParsing';
  import {layerSchemasToJsonSchemas} from '@/utils/LayerSchemaSaving';

  @Component({
    components: {ParamsList, Constraints, VRuntimeTemplate, CloseButton}
  })
  export default class Admin extends Vue {
    layerSchemas: LayerSchema[] = [];
    JSONTypes = JSONTypes;

    saveSchemas() {
      console.log("OK!");
      const results = layerSchemasToJsonSchemas(this.layerSchemas);
      (<any>window).RESULTS = results;
    }


    deleteLayerSchema(lSchema: LayerSchema) {
      this.layerSchemas!.splice(this.layerSchemas!.indexOf(lSchema), 1);
    }

    addLayerSchema(event: MouseEvent) {
      this.layerSchemas!.push(LayerSchema.createDefault());
    }

    mounted() {
      console.log("MOUNTED!");
      Axios
        .get(backendUrls.getLayersSchemas)
        .then(
          response => {
            console.log(response);
            this.layerSchemas = parseLayersSchemas(response.data);
          },
          err => {
            if (err.status == 401) {
              this.$router.push({name: 'login', params: {msg: 'LOGIN EXPIRED'}});
            }
          });
    }
  }


</script>

<style>

</style>