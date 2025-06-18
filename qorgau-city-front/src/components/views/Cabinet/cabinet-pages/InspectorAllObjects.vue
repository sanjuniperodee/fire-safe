<script setup lang="ts">
import ObjectsInspector from '@views/Objects/objects-inspector/ObjectsInspector.vue'
import CabinetInspectorLayout from '@/layouts/CabinetInspectorLayout.vue'
import CabinetInfo from '@views/Cabinet/cabinet-info/CabinetInfo.vue'
</script>

<template>
    <div class="cabinet-info"><CabinetInfo /></div>
    <div class="main">
      <ObjectsInspector />
    </div>
</template>

<style scoped lang="scss">
.main {
  height: calc(100vh - 56px);
  padding: 20px 0;
}
.cabinet-info {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

@media only screen and (max-width: 789px) {
  .main {
    left: 0;
    padding: 0 10px;
  }
  .cabinet-info {
    display: none;
  }
}
</style>
