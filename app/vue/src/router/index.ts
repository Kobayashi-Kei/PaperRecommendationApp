import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SearchResult from '../views/SearchResult.vue'
import PaperDetail from '../views/PaperDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: Home
    },
    {
      path: '/searchResult',
      name: 'searchResult',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: SearchResult
    },
    {
      path: '/paperDetail',
      name: 'PaperDetail',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: PaperDetail
    },
  ]
})

export default router
