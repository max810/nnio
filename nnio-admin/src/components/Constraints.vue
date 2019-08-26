<template>
  <div>
    {{ param.name }} constraints
    <atomic-constraints v-if="param.type !== 'object'" v-bind:param="param"></atomic-constraints>
    <params-list v-else v-bind:params="param.additionalConstraints" v-bind:baseId="baseId"></params-list>
  </div>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import LayerParam from '@/classes/LayerParam';
  import AtomicConstraints from '@/components/AtomicConstraints.vue';
  import ParamsList from '@/components/ParamsList.vue';

  @Component({
    components: {ParamsList, AtomicConstraints}
  })
  export default class Constraints extends Vue {
    @Prop(LayerParam) param: LayerParam | undefined;
    @Prop(String) baseId: string | undefined;
    name = "constraints";
  }

</script>

<style scoped>

</style>