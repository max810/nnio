<template>
  <div>
    <table class="table atomic" v-if="['number', 'integer'].includes(param.type)">
      <tr>
        <td class="col">
          <input type="number" v-model.number="param.additionalConstraints.minimum">
        </td>
        <td style="min-width: 150px; text-align: center">
          <label><= Value <=</label>
        </td>
        <td>
          <input type="number" v-model.number="param.additionalConstraints.maximum">
        </td>
      </tr>
    </table>
    <table class="table" v-if="['string', 'boolean'].includes(param.type)">

    </table>
    <table class="table" v-if="['array'].includes(param.type)">
      <tr>
        <td>
          <input type="number" min="0" v-model.number="param.additionalConstraints.minItems">
        </td>
        <td style="min-width: 150px; text-align: center">
          <label><= # of items <=</label>
        </td>
        <td>
          <input type="number" min="0" v-model.number="param.additionalConstraints.maxItems">
        </td>
      </tr>
      <tr>
        <td colspan="2" style="text-align: right">
          Type of items
        </td>
        <td>
          <select v-model="param.additionalConstraints.itemsType">
            <option></option>
            <option v-for="t of JSONTypes">
              {{ t }}
            </option>
          </select>
        </td>
      </tr>
    </table>
  </div>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import {JSONTypes} from "@/constants";
  import LayerParam from '@/classes/LayerParam';

  @Component({})
  export default class AtomicConstraints extends Vue {
    JSONTypes = JSONTypes;
    @Prop(LayerParam) param: LayerParam | undefined;
  }
</script>

<style scoped>

</style>