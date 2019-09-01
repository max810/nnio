<template>
  <button type="button" class="close" aria-label="Close" v-on:click="clicked">
    <span aria-hidden="true">&times;</span>
  </button>
</template>

<script lang="ts">
  import {Component, Vue} from 'vue-property-decorator';

  @Component({})
  export default class CloseButton extends Vue {
    clicked(event: MouseEvent) {
      this.$emit('click');
    }
  }
</script>

<style scoped>

</style>