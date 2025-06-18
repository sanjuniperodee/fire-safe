<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref, onMounted, onUnmounted } from 'vue'
import { close, menu, house, people, tools, settingSvg, person } from '@/assets/svg'

const router = useRouter()
const navbarClosed = ref(false)
const isMobile = ref(false)

const goToPage = (route: string) => {
  router.push({ name: route })
}

const emit = defineEmits(['navbar-toggle'])

const toggleNavbar = () => {
  navbarClosed.value = !navbarClosed.value
  emit('navbar-toggle', navbarClosed.value)
}

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (isMobile.value) {
    navbarClosed.value = true
  }
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<template>
  <nav
    class="navbar"
    :class="{ 'navbar-closed': navbarClosed, mobile: isMobile }"
  >
    <button
      class="toggle-btn"
      @click="toggleNavbar()"
      v-html="navbarClosed ? menu : close"
    ></button>

    <div class="navs-wrapper">
      <button
        class="custom-btn"
        @click="goToPage('Profile')"
      >
        <span v-html="person"></span>
        <span v-if="!navbarClosed">Профиль</span>
      </button>

      <!-- <button
        class="custom-btn"
        @click="goToPage('InspectorAllObjects')"
      >
        <span v-html="house"></span>
        <span v-if="!navbarClosed">Объекты</span>
      </button>

      <button
        class="custom-btn"
        @click="goToPage('InspectorNotedObjects')"
      >
        <span v-html="house"></span>
        <span v-if="!navbarClosed">Мои Объекты</span>
      </button> -->

      <button
        class="custom-btn"
        @click="goToPage('Citizens')"
      >
        <span v-html="people"></span>
        <span v-if="!navbarClosed">Граждане</span>
      </button>

      <!-- <button
        class="custom-btn"
        @click="goToPage('Providers')"
      >
        <span v-html="tools"></span>
        <span v-if="!navbarClosed">Поставщики</span>
      </button> -->

      <button class="custom-btn">
        <span v-html="settingSvg"></span>
        <span v-if="!navbarClosed">Настройки</span>
      </button>
    </div>
  </nav>
</template>

<style scoped lang="scss">
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 250px;
  background-color: #f37b01;
  color: #fff;
  transition: all 0.4s ease-in-out;
  z-index: 1000;

  &.navbar-closed {
    width: 64px;
  }

  &.mobile {
    width: 100%;
    height: 100vh;

    &.navbar-closed {
      width: 64px;
      height: 100%;
    }
  }

  .navs-wrapper {
    width: 100%;
    display: flex;
    flex-direction: column;
    margin-top: 64px;
    font-size: 18px;
    font-weight: 500;
    text-align: left;
  }

  .navs-wrapper button {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 15px;
    padding: 15px 30px;
    width: 100%;
  }

  .navs-wrapper button:hover {
    background-color: #f58d25;
  }

  .toggle-btn {
    position: absolute;
    top: 0;
    right: 0;
    height: 64px;
    width: 64px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    background: none;
    border: none;
    color: inherit;
  }

  .custom-btn {
    display: flex;
    align-items: center;
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
  }

  &.navbar-closed {
    .navs-wrapper button {
      justify-content: center;
      padding: 15px 0;
    }

    .custom-btn span:first-child {
      margin: 0 auto;
    }
  }
}

@media (max-width: 768px) {
  .navbar {
    &:not(.navbar-closed) {
      .navs-wrapper {
        align-items: center;
      }

      .custom-btn {
        justify-content: center;
      }
    }
  }
}
</style>
