<template>
  <div>
    <table class="table atomic">
      <tr v-for="entry of param.oneOfs"> <!-- entry must be {type:'', value: ''} object -->
        <td>
          <atomic-param-value-input v-bind:param="entry" v-bind:paramType="entry.type"></atomic-param-value-input>
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
  import AtomicParamValueInput from '@/components/AtomicParamValueInput.vue';
  import LayerParam from '@/classes/LayerParam';

  @Component({
    components: {AtomicParamValueInput}
  })
  export default class AtomicOneOfs extends Vue {
    JSONTypes = JSONTypes;
    @Prop(LayerParam) param: LayerParam | undefined;
  }
</script>

<style scoped>

</style>