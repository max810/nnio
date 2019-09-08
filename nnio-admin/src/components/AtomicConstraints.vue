<template>
  <div>
    <table class="table atomic" v-if="['number', 'integer'].includes(param.type)">
      <tr>
        <td>
          <input type="number" v-model.number="param.activeConstraints.minimum">
        </td>
        <td style="min-width: 150px; text-align: center">
          <label><= Value <=</label>
        </td>
        <td>
          <input type="number" v-model.number="param.activeConstraints.maximum">
        </td>
      </tr>
    </table>
    <table class="table" v-else-if="['string', 'boolean'].includes(param.type)">

    </table>
    <table class="table" v-else-if="['array'].includes(param.type)">
      <tr>
        <td>
          <input type="number" min="0" v-model.number="param.activeConstraints.minItems">
        </td>
        <td style="min-width: 150px; text-align: center">
          <label><= # of items <=</label>
        </td>
        <td>
          <input type="number" min="0" v-model.number="param.activeConstraints.maxItems">
        </td>
      </tr>
      <tr>
        <td colspan="2" style="text-align: right">
          Type of items
        </td>
        <td>
          <select v-model="param.activeConstraints.itemsConstraints.type">
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
  import LayerParam from "@/classes/LayerParam";

  @Component({})
  export default class AtomicConstraints extends Vue {
    JSONTypes = JSONTypes;
    @Prop(LayerParam) param: LayerParam | undefined;
  }
</script>

<style scoped>

</style>