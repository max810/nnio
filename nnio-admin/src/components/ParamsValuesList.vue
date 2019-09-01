<template>
  <table class="table table-bordered">
    <tr v-for="param of params">
      <td class="fit" v-if="withNames">
        <input type="text"
               v-model="param.name">
      </td>
      <td>
        <atomic-param-value-input v-if="param.type !== 'object' && param.type !== 'array'" v-bind:param="param"
                                  v-bind:paramType="param.type"></atomic-param-value-input>
        <params-values-list v-else v-bind:withNames="param.type !== 'array'" v-bind:params="param.value"
                            v-bind:baseId="`inner-` + baseId"></params-values-list>
      </td>
      <td>
        <close-button v-on:click="deleteLayerParamValue(param)"></close-button>
      </td>
    </tr>
    <tr>
      <td>
        <button v-on:click="addNewParam">
          <span v-if="withNames">Add param</span>
          <span v-else>Add item</span>
        </button>
      </td>
    </tr>
  </table>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import LayerParam from '@/classes/LayerParam';
  // import Constraints from '@/components/Constraints.vue';
  import {JSONTypes} from "@/constants";
  import LayerParamValue from "@/classes/LayerParamValue";
  import AtomicParamValueInput from '@/components/AtomicParamValueInput.vue';
  import CloseButton from '@/components/CloseButton.vue';

  @Component({
    components: {CloseButton, AtomicParamValueInput}

    // components: {Constraints}
  })
  export default class ParamsValuesList extends Vue {
    @Prop(Array) params: LayerParamValue[] | undefined;
    @Prop(String) baseId: string | undefined;
    @Prop({type: Boolean, default: false}) withNames: boolean | undefined;
    JSONTypes = JSONTypes;
    name = "params-values-list";

    beforeCreate() {
      if (this.$options.components) {
        this.$options.components.Constraints = require("@/components/Constraints").default;
      } else {
        console.log("FAILED FAILED FAILED IMPORT CONSTRAINTS");
      }
    }

    addNewParam(event: MouseEvent) {
      this.params!.push(LayerParamValue.createDefault());
    }

    deleteLayerParamValue(param: LayerParamValue) {
      this.params!.splice(this.params!.indexOf(param), 1);
    }

  }

</script>

<style scoped>
  input {
    margin: 0 0.3rem;
  }


</style>