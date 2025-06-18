<template>
  <div
    class="map"
    :id="rootId"
  ></div>
</template>

<script setup lang="ts">
defineProps<{
  rootId: string
}>()
</script>

<style>
.cluster-icon {
  width: 40px;
  height: 40px;
  background-color: rgb(187, 187, 187);
  color: black;
  display: flex;
  font-size: 18px;
  font-weight: 700;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
}

.map {
  height: 100%;
  width: 100vw;
}

.mark {
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: start;
  font-size: 18px;
  width: 500px;
}

.mark__title {
  font-weight: 700;
  letter-spacing: 0.8px;
  line-height: normal;
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid #ccc;
  width: 100%;
}

.mark__field {
  font-weight: 500;
}

.mark__field-row {
  display: flex;
  gap: 4px;
}

.pac-card {
  background-color: #fff;
  border: 0;
  border-radius: 2px;
  box-shadow: 0 1px 4px -1px rgba(0, 0, 0, 0.3);
  margin: 10px;
  padding: 0 0.5em;
  overflow: hidden;
  padding: 0;
}

#pac-container {
  padding-bottom: 12px;
  margin-right: 12px;
  opacity: 0.5;
}

.pac-controls {
  display: inline-block;
  padding: 5px 11px;
}

.pac-controls label {
  font-family: Roboto;
  font-size: 13px;
  font-weight: 300;
}

#pac-input {
  background-color: #fff;
  font-size: 15px;
  font-weight: 300;
  margin-left: 12px;
  color: #000;
  border-radius: 10px;
  filter: drop-shadow(2px 2px 2px #ffffff2f);
  margin-top: 10px;
  padding: 12px 15px 10px 15px;
  text-overflow: ellipsis;
  width: 600px;
}

#pac-input:focus {
  border-color: #4d90fe;
}
</style>
