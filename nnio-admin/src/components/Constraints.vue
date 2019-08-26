<template>
  <div>
    {{ param.name }} constraints
    <atomic-constraints v-if="param.type !== 'object'" v-bind:param="param"></atomic-constraints>
    <table v-else class="table">
      <tr>
        <td>TODO ;;;))) (add params-list)</td>
      </tr>
    </table>
  </div>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import LayerParam from '@/classes/LayerParam';
  import AtomicConstraints from '@/components/AtomicConstraints.vue';

  @Component({
    components: {AtomicConstraints}
  })
  export default class Constraints extends Vue {
    @Prop(LayerParam) param: LayerParam | undefined;
    name = "constraints";
  }

</script>

<style scoped>

</style>