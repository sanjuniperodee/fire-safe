<script setup lang="ts">
import { ref } from 'vue'
import { useStatementStore } from '@stores/StatementsStore'

const props = defineProps<{
  limit: number
  offset: number
}>()

const minPrice = ref(0)
const maxPrice = ref(99999)
const selectedFilter = ref('newItems')
const statementStore = useStatementStore()

const handleApply = async () => {
  const seen = ref(false)

  if (selectedFilter.value === 'newItems') {
    seen.value = false
  } else if (selectedFilter.value === 'seen') {
    seen.value = true
  }

  const limit = props.limit
  const offset = props.offset

  const min_price = minPrice.value
  const max_price = maxPrice.value

  await statementStore.getAllStatementsFiltered(
    limit,
    offset,
    min_price,
    max_price,
    seen.value
  )
}

</script>

<template>
  <div class="filter-content">
    <h2>Фильтр</h2>
    <form class="form">
      <div class="filter-point">
        <input type="radio" name="filter" value="newItems" v-model="selectedFilter">
        <p class="filter-point-p">Сначала новые</p>
      </div>
      <div class="filter-point">
        <input type="radio" name="filter" value="seen" v-model="selectedFilter">
        <p class="filter-point-p">Сначала просмотренные</p>
      </div>
    </form>

    <div class="price-wrapper">
      <label>Цена:</label>
      <div class="price-range">
        <label>от</label>
        <div class="textInputWrapper">
          <input
            v-model.number="minPrice"
            placeholder="от"
            type="number"
            class="textInput"
            required
          />
        </div>

        <label>до</label>
        <div class="textInputWrapper">
          <input
            v-model.number="maxPrice"
            placeholder="до"
            type="number"
            class="textInput"
            required
          />
        </div>
      </div>
    </div>
    <button @click="handleApply" class="apply-btn">Применить</button>
  </div>
</template>

<style scoped lang="scss">
.filter-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 5px 5px rgba(0,0,0,0.2);
  background-color: white;
  border-radius: 10px;
  padding: 50px 30px;
  width: 30%;

  max-height: 500px;
  position: sticky;
  top: 50px;
}

.form {
  margin: 10px 0;
  height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.price-wrapper {
  margin: 10px 0;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-point {
  display: flex;
  align-items: center;
  gap: 10px;
}
.filter-point-p{
  padding-top: 4px;
}

.apply-btn {
  background-color: #333;
  color: white;
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

h2{
  font-size: 24px;
  font-weight: 500;
  padding-bottom: 10px;
  border-bottom: 1px solid #dadada;
}

@media only screen and (max-width: 920px) {
  .filter-content {
    width: 90%;
    height: 300px;
    padding: 20px;
    margin: 171px 0;
    top: 0;
  }
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}

.textInputWrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
  width: 50%;
  margin: 12px 5px;
  --accent-color: #ff9800;
}

.textInputWrapper:before,
.textInputWrapper:after {
  content: '';
  left: 0;
  right: 0;
  position: absolute;
  pointer-events: none;
  bottom: -1px;
  z-index: 4;
  width: 100%;
}

.textInputWrapper:before {
  transition: border-bottom-color 200ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
  border-bottom: 1px solid rgba(255, 255, 255, 0.42);
}

.textInputWrapper:focus-within:before {
  border-bottom: 1px solid var(--accent-color);
  transform: scaleX(1);
}

.textInputWrapper:after {
  content: '';
  transform: scaleX(0);
  transition: transform 250ms cubic-bezier(0, 0, 0.2, 1) 0ms;
  will-change: transform;
  border-bottom: 2px solid var(--accent-color);
  border-bottom-color: var(--accent-color);
}

.textInputWrapper:focus-within:after {
  border-bottom: 2px solid var(--accent-color);
  transform: scaleX(1);
}

.textInput::placeholder {
  transition: opacity 250ms cubic-bezier(0, 0, 0.2, 1) 0ms;
  opacity: 1;
  user-select: none;
  color: rgba(255, 255, 255, 0.582);
}

.textInputWrapper .textInput {
  border-radius: 5px 5px 0 0;
  box-shadow: 0 2px 5px rgb(35 35 35 / 30%);
  max-height: 36px;
  background-color: #ffffff; /* Белый цвет */
  transition-timing-function: cubic-bezier(0.25, 0.8, 0.25, 1);
  transition-duration: 200ms;
  transition-property: background-color;
  color: #000000; /* Черный цвет текста */
  font-size: 14px;
  font-weight: 500;
  padding: 12px;
  width: 100%;
  border-left: none;
  border-bottom: none;
  border-right: none;
}

.textInputWrapper .textInput:focus,
.textInputWrapper .textInput:active {
  outline: none;
}

.textInputWrapper:focus-within .textInput::placeholder {
  opacity: 0;
}

</style>
