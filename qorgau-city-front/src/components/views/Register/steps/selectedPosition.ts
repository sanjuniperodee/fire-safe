import { ref } from 'vue';
import { positionTypesMapping } from '@/types/User';
// @ts-expect-error
import { userPosition } from './RoleSelect.vue';

// Явное приведение типа userPosition.value к ключу объекта positionTypesMapping
export const selectedPosition = ref(
  positionTypesMapping[userPosition.value as keyof typeof positionTypesMapping]
);