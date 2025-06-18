<script setup lang="ts">
import { ref } from 'vue'
import CabinetNavbar from '@views/Cabinet/cabinet-navbar/CabinetNavbar.vue'
import CabinetInfo from '@views/Cabinet/cabinet-info/CabinetInfo.vue'

const isNavbarOpen = ref(true)

const handleNavbarToggle = (closed: boolean) => {
  isNavbarOpen.value = !closed
}
</script>

<template>
  <div
    class="wrapper"
    :class="{ 'navbar-closed': !isNavbarOpen }"
  >
    <CabinetNavbar @navbar-toggle="handleNavbarToggle" />

    <div class="main-content">
      <div class="content">
        <slot></slot>
      </div>
      <div class="cabinet-info"><CabinetInfo /></div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.wrapper {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: margin-left 0.4s ease-in-out;
}

.content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
}

.cabinet-info {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.wrapper:not(.navbar-closed) .main-content {
  margin-left: 250px;
}

.wrapper.navbar-closed .main-content {
  margin-left: 64px;
}

@media only screen and (max-width: 768px) {
  .wrapper:not(.navbar-closed) .main-content {
    margin-left: 0;
  }

  .wrapper.navbar-closed .main-content {
    margin-left: 64px;
  }

  .cabinet-info {
    display: none;
  }
}
</style>
