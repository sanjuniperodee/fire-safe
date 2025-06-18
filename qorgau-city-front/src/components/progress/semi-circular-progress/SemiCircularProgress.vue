<template>
  <div class="flex-col">
    <div
      class="semi-donut margin"
      :style="{ '--percentage': percentage }"
      style="--fill: #ff3d00"
    >
      <v-icon>{{ icon }}</v-icon>
      <span class="title">{{ percentage }}%</span>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  percentage: {
    type: Number,
    required: true,
    default: 0
  },
  icon: String
})
</script>

<style lang="scss" scoped>
.semi-donut {
  --percentage: 0;
  --fill: #ff0;
  width: 300px;
  height: 150px;
  position: relative;
  color: #fff;
  font-size: 50px;
  gap: 8px;
  font-weight: 600;
  overflow: hidden;
  color: #3f3f46;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  box-sizing: border-box;

  &:after {
    content: '';
    width: 200px;
    height: 200px;
    border: 5px solid;
    border-color: rgba(0, 0, 0, 0.15) rgba(0, 0, 0, 0.15) $green $green;
    position: absolute;
    border-radius: 50%;
    left: 10;
    top: 0;
    box-sizing: border-box;
    transform: rotate(calc(1deg * (-45 + var(--percentage) * 1.8)));
    animation: fillAnimation 1s ease-in;
  }

  &:before {
    content: '';
    width: 200px;
    height: 200px;
    border: 20px solid;
    border-color: $yellow $green $red $red;
    position: absolute;
    border-radius: 50%;
    left: 10;
    top: 0;
    box-sizing: border-box;
    transform: scale(0.95);
  }
}

@keyframes fillAnimation {
  0% {
    transform: rotate(-45deg);
  }

  50% {
    transform: rotate(135deg);
  }
}

.flex-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.title {
  width: 300px;
  text-align: center;
  font-size: 24px;
  font-weight: 700;
  font-family: 'Overpass', sans-serif;
}
</style>
