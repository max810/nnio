<template>
  <input v-if="['number', 'integer'].includes(paramType)" type="number"
         v-model.number="param.activeValue">
  <input v-else-if="['string'].includes(paramType)" type="text"
         v-model="param.activeValue">
  <select v-else-if="['boolean'].includes(paramType)"
          v-model="param.activeValue">
    <option></option>
    <option>true</option>
    <option>false</option>
  </select>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import {JSONTypes} from "@/constants";
  import NamelessLayerParamValue from '@/classes/NamelessLayerParamValue';

  @Component({})
  export default class AtomicParamValueInput extends Vue {
    JSONTypes = JSONTypes;
    @Prop(NamelessLayerParamValue) param: NamelessLayerParamValue | undefined;
    @Prop(String) paramType: string | undefined;
    // addItemTo
  }
</script>

<style scoped>

</style>