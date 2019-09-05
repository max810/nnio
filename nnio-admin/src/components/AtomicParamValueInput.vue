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
  <!--    <table v-else-if="['array'].includes(paramType)">-->
  <!--      <tr v-for="item of param">-->
  <!--        <td>-->
  <!--          <input v-model="item.value">-->
  <!--          Type:-->
  <!--          <select v-model="item.type">-->
  <!--            <option v-for="t of JSONTypes">-->
  <!--              {{ t }}-->
  <!--            </option>-->
  <!--          </select>-->
  <!--        </td>-->
  <!--      </tr>-->
  <!--      <tr>-->
  <!--        <td>-->
  <!--          <button>TODO Add 1</button>-->
  <!--        </td>-->
  <!--      </tr>-->
  <!--    </table>-->
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