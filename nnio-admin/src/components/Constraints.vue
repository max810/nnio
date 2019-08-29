<template>
  <div>
    <!--    {{ param.name }} constraints-->
    <table>
      <tr>
        <td>
          <label>
            <input type="radio" v-bind:checked="!param.isOneOf" v-on:click="param.isOneOf = false">
            Constraints
          </label>
        </td>
        <td>
          <label>
            <input type="radio" v-bind:checked="param.isOneOf" v-on:click="param.isOneOf = true">
            One of
          </label>
        </td>
      </tr>
    </table>
    <div v-if="!param.isOneOf">
      <atomic-constraints v-if="param.type !== 'object'" v-bind:param="param"></atomic-constraints>
      <params-list v-else v-bind:params="param.additionalConstraints" v-bind:baseId="baseId"></params-list>
    </div>
    <div v-else>
      <atomic-one-ofs v-if="param.type !== 'object'" v-bind:param="param"></atomic-one-ofs>
      <div v-else>TODO oneOf for object ;)</div>
      <!--      <atomic-one-ofs v-if="param.type !== 'object'" v-bind:param="param"></atomic-one-ofs>-->
    </div>
  </div>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import LayerParam from '@/classes/LayerParam';
  import AtomicConstraints from '@/components/AtomicConstraints.vue';
  import ParamsList from '@/components/ParamsList.vue';
  import AtomicOneOfs from '@/components/AtomicOneOfs.vue';

  @Component({
    components: {AtomicOneOfs, ParamsList, AtomicConstraints}
  })
  export default class Constraints extends Vue {
    @Prop(LayerParam) param: LayerParam | undefined;
    @Prop(String) baseId: string | undefined;
    name = "constraints";
  }

</script>

<style scoped>

</style>