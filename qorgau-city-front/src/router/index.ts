import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/objects',
      name: 'Objects',
      component: () => import('@views/Objects/ObjectsView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/objects/view/:id',
      name: 'ObjectOwner',
      component: () =>
        import(
          '@views/Objects/objects-owner/pages-with-params/object-owner-inspect/ObjectOwnerView.vue'
        ),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/objects/edit/:id',
      name: 'ObjectOwnerEdit',
      component: () =>
        import(
          '@views/Objects/objects-owner/pages-with-params/object-owner-edit/ObjectOwnerEditView.vue'
        ),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/objects/view/:id/:subBuilding',
      name: 'SubBuildingInfo',
      component: () => import('@views/SubBuilding/SubBuildingInfo.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/objects/edit/:id/:subBuilding',
      name: 'SubBuildingEditInfo',
      component: () => import('@views/SubBuilding/SubBuildingEditInfo.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/objects/edit/:id/document/:documentTitle',
      name: 'DocumentPage',
      component: () =>
        import(
          '@views/Objects/objects-owner/pages-with-params/object-owner-edit/forms/steps/ObjectOwnerEditDocument.vue'
        ),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@views/Profile/ProfileView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/cabinet',
      name: 'Cabinet',
      component: () => import('@views/Cabinet/CabinetView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/providerCabinet',
      name: 'ProviderCabinet',
      component: () => import('@views/ProviderCabinet/ProviderCabinet.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/cabinet/inspectorAllObjects',
      name: 'InspectorAllObjects',
      component: () => import('@views/Cabinet/cabinet-pages/InspectorAllObjects.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/cabinet/inspectorNotedObjects',
      name: 'InspectorNotedObjects',
      component: () => import('@views/Cabinet/cabinet-pages/InspectorNotedObjects.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/cabinet/citizens',
      name: 'Citizens',
      component: () => import('@views/Cabinet/cabinet-pages/CabinetCitizens.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/cabinet/providers',
      name: 'Providers',
      component: () => import('@views/Cabinet/cabinet-pages/CabinetProviders.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/providers/view/:id',
      name: 'ProviderInfo',
      component: () => import('@views/ProviderCabinet/ProviderInfo.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/advertisements',
      name: 'Advertisements',
      component: () => import('@views/Advertisements/AdvertisementsView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/advertisements/view/:id',
      name: 'AdvertisementFullInfo',
      component: () => import('@views/Advertisements/AdvertisementFullInfo.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/createAdvertisements',
      name: 'CreateAdvertisements',
      component: () => import('@views/Advertisements/CreateAdvertisements.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/statements',
      name: 'Statements',
      component: () => import('@views/Statements/StatementsView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/statements/selected',
      name: 'SelectedStatements',
      component: () => import('@views/Statements/SelectedStatements/SelectedStatemens.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/statement/view/:id',
      name: 'StatementById',
      component: () => import('@views/Statements/StatementPage/StatementById.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/statement/edit/:id',
      name: 'StatementEdit',
      component: () => import('@views/Statements/StatementEdit/StatementEdit.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/myStatements',
      name: 'MyStatements',
      component: () => import('@views/Statements/MyStatements/MyStatements.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/chat',
      name: 'Chat',
      component: () => import('@views/Chat/ChatView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@views/Login/LoginView.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@views/Register/RegisterView.vue')
    },
    {
      path: '/map',
      name: 'Map',
      component: () => import('@views/Map/MapView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/admin-building',
      name: 'AdminObject',
      component: () => import('@views/AdminObject/AdminObjectView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/faq',
      name: 'Faq',
      component: () => import('@views/Faq/FaqView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/forgot-password',
      name: 'ForgotPassword',
      component: () => import('@views/Login/ForgotPassword/ForgotPasswordView.vue')
    },
    {
      path: '/code-verification',
      name: 'CodeVerification',
      component: () => import('@views/Register/CodeVerification/CodeVerificationView.vue'),
    },
    {
      path: '/',
      name: 'Home',
      component: () => import('@views/Home/HomeView.vue'),
      meta: {
        requiresAuth: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  console.log(isAuthenticated)
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' })
  } else {
    next()
  }
})
export default router
