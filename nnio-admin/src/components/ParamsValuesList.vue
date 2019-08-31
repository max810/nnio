<template>
  <table class="table table-bordered">
    <tr v-for="param of params">
      <td class="fit">
        <input type="text"
               v-model="param.name">
      </td>
      <td>
        <atomic-param-value-input v-if="param.type !== 'object'" v-bind:param="param"
                                  v-bind:paramType="param.type"></atomic-param-value-input>
        <div v-else v-for="prop of param.value">
          <params-values-list v-bind:params="prop.value" v-bind:baseId="`inner-` + baseId"></params-values-list>
        </div>
      </td>
    </tr>
    <tr>
      <td>TODO add</td>
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

  @Component({
    components: {AtomicParamValueInput}

    // components: {Constraints}
  })
  export default class ParamsValuesList extends Vue {
    @Prop(Array) params: LayerParamValue[] | undefined;
    @Prop(String) baseId: string | undefined;
    JSONTypes = JSONTypes;
    name = "params-values-list";

    beforeCreate() {
      if (this.$options.components) {
        this.$options.components.Constraints = require("@/components/Constraints").default;
      } else {
        console.log("FAILED FAILED FAILED IMPORT CONSTRAINTS");
      }
    }
  }

</script>

<style scoped>
  input {
    margin: 0 0.3rem;
  }


</style>