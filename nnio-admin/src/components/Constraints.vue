<template>
  <div>
<!--        {{ param.name }} constraints-->
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
      <params-list v-else v-bind:params="param.activeConstraints"
                   v-bind:baseId="baseId"></params-list>
      <div v-if="param.type === 'array'">
        Constraints for array items:
        <constraints v-bind:param="param.activeConstraints.itemsConstraints"
                     v-bind:baseId="`items-${baseId}`"></constraints>
      </div>
    </div>
    <div v-else>
      <atomic-one-ofs v-if="!['object', 'array'].includes(param.type)" v-bind:items="param.activeOneOfs"
                      v-bind:itemsType="param.type"></atomic-one-ofs>
      <div v-else>
        <params-values-list
            v-for="item of param.activeOneOfs"
            v-bind:params="item"
            v-bind:baseId="`oneOfs-` + baseId.toString()"
            v-bind:withNames="param.type !== 'array'"></params-values-list>
        <button v-on:click="addNewOneOfObject">
          Add oneOfs item
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import LayerParam from '@/classes/LayerParam';
  import AtomicConstraints from '@/components/AtomicConstraints.vue';
  import ParamsValuesList from '@/components/ParamsValuesList.vue';
  import ParamsList from '@/components/ParamsList.vue';
  import AtomicOneOfs from '@/components/AtomicOneOfs.vue';
  import {JSONDefaults} from '@/constants';

  @Component({
    components: {AtomicOneOfs, ParamsValuesList, AtomicConstraints, ParamsList}
  })
  export default class Constraints extends Vue {
    @Prop(LayerParam) param: LayerParam | undefined;
    @Prop(String) baseId: string | undefined;
    name = "constraints";

    addNewOneOfObject(event: MouseEvent) {
      this.param!.activeOneOfs.push([]);
    }
  }

</script>

<style scoped>

</style>