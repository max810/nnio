<template>
  <table class="table table-bordered">
    <tr v-for="param of params">
      <td class="fit">
        <input type="text"
               v-model="param.name">
      </td>
      <td>
        <div class="form-check form-check-inline">
          <label>
            Type:
            <select v-model="param.type"
                    class="">
              <option v-for="t of JSONTypes">
                {{ t }}
              </option>
            </select>
          </label>
          <label class="form-check-label">
            <input type="checkbox" v-model="param.required">
            Required
          </label>
        </div>
        <div>
          <a
              class
              data-toggle="collapse"
              v-bind:href="`#${collapseBaseId}-${param.name}-additional-constraints`"
              role="button"
              aria-expanded="false"
              aria-controls="collapseExample">
            Additional constraints
          </a>
          <div
              class="collapse"
              v-bind:id="`${collapseBaseId}-${param.name}-additional-constraints`">
            <div class="card card-body">
              <!--TODO: when changed param type, DO NOT DELETE previous type's constraints.
                    Instead during saving just `switch` over type and take needed constraints
                  -->
              <constraints v-bind:param="param"></constraints>
            </div>
          </div>
        </div>
      </td>
    </tr>
  </table>
</template>

<script lang="ts">
  import {Component, Prop, Vue} from 'vue-property-decorator';
  import LayerParam from '@/classes/LayerParam';
  import Constraints from '@/components/Constraints.vue';
  import {JSONTypes} from "@/constants";

  @Component({
    components: {Constraints}
  })
  export default class ParamsList extends Vue {
    @Prop(Array) params: LayerParam[] | undefined;
    @Prop(String) collapseBaseId: string | undefined;
    JSONTypes = JSONTypes;
    name = "params-list";
  }

</script>

<style scoped>
  input {
    margin: 0 0.3rem;
  }


</style>