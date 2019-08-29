<template>
  <div>
    <table class="table atomic">
      <tr v-for="entry of param.oneOfs"> <!-- entry must be {type:'', value: ''} object -->
        <td>
          <input v-if="['number', 'integer'].includes(param.type)" type="number"
                 v-model.number="entry.value">
          <input v-else-if="['string'].includes(param.type)" type="number"
                 v-model="entry.value">
          <select v-else-if="['boolean'].includes(param.type)" type="number"
                  v-model.number="entry.value">
            <option></option>
            <option>true</option>
            <option>false</option>
          </select>
          <table v-else-if="['array'].includes(param.type)">
            <tr v-for="item of entry">
              <input v-model="item.value">
              Type:
              <select v-model="param.type">
                <option v-for="t of JSONTypes">
                  {{ t }}
                </option>
              </select>
            </tr>
            <tr>
              TODO add ({type: '', value: ''})
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        TODO add
      </tr>
    </table>
  </div>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import {JSONTypes} from "@/constants";
  import LayerParam from '@/classes/LayerParam';

  @Component({})
  export default class AtomicOneOfs extends Vue {
    JSONTypes = JSONTypes;
    @Prop(LayerParam) param: LayerParam | undefined;
  }
</script>

<style scoped>

</style>