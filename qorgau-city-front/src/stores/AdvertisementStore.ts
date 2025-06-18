// import { defineStore } from 'pinia';
// import { ref } from 'vue';
// import { advertisementService } from '@/services/advertisements.service';
// import type { Advertisement } from '@/types/Advertisements';
//
// export const useAdvertisementStore = defineStore('advertisementStore', () => {
//   const advertisements = ref<Advertisement[]>([]);
//   const loading = ref(false);
//   const error = ref<string | null>(null);
//
//   const getAdvertisements = async () => {
//     loading.value = true;
//     error.value = null;
//     try {
//       advertisements.value = await advertisementService.getAdvertisements();
//     } catch (err) {
//       error.value = 'Ошибка загрузки объявлений';
//       console.error('Ошибка загрузки объявлений:', err);
//     } finally {
//       loading.value = false;
//     }
//   };
//
//   const filterAdvertisements = (category: string) => {
//     return advertisements.value.filter(ad => ad.category === category);
//   };
//
//   return {
//     advertisements,
//     loading,
//     error,
//     getAdvertisements,
//     filterAdvertisements,
//   };
// });
