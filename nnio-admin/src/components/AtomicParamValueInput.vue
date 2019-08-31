<template>
  <div>
    <input v-if="['number', 'integer'].includes(paramType)" type="number"
           v-model.number="param.value">
    <input v-else-if="['string'].includes(paramType)" type="text"
           v-model="param.value">
    <select v-else-if="['boolean'].includes(paramType)"
            v-model="param.value">
      <option></option>
      <option>true</option>
      <option>false</option>
    </select>
    <table v-else-if="['array'].includes(paramType)">
      <tr v-for="item of param">
        <input v-model="item.value">
        Type:
        <select v-model="paramType">
          <option v-for="t of JSONTypes">
            {{ t }}
          </option>
        </select>
      </tr>
      <tr>
        TODO add ({type: '', value: ''})
      </tr>
    </table>
  </div>
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
  }
</script>

<style scoped>

</style>