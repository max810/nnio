<template>
  <table class="table atomic">
    <tr v-for="entry of items">
      <td>
        <atomic-param-value-input v-bind:param="entry" v-bind:paramType="itemsType"></atomic-param-value-input>
      </td>
      <td>
        <close-button v-on:click="deleteEntry(entry)"></close-button>
      </td>
    </tr>
    <tr>
      <td>
        <button v-on:click="addOneOf">Add atomic oneOf item</button>
      </td>
    </tr>
  </table>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import {JSONDefaults, JSONTypes} from "@/constants";
  import AtomicParamValueInput from '@/components/AtomicParamValueInput.vue';
  import LayerParam from '@/classes/LayerParam';
  import NamelessLayerParamValue from "@/classes/NamelessLayerParamValue";
  import CloseButton from '@/components/CloseButton.vue';

  @Component({
    components: {CloseButton, AtomicParamValueInput}
  })
  export default class AtomicOneOfs extends Vue {
    JSONTypes = JSONTypes;
    @Prop(Array) items: any[] | undefined;
    @Prop(String) itemsType: string | undefined;

    addOneOf(event: MouseEvent) {
      const type_ = this.itemsType!;
      this.items!.push(new NamelessLayerParamValue(type_, JSONDefaults[type_]));
    }

    deleteEntry(entry: any) {
      this.items!.splice(this.items!.indexOf(entry), 1);
    }
  }
</script>

<style scoped>

</style>