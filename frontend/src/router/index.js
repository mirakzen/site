import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'MainView',
            component: () => import('../views/Main.vue'),
            meta: {
                title: 'mirakzen'
            }
        },
        {
            path: '/projects',
            name: 'ProjectsView',
            component: () => import('../views/Projects.vue'),
            meta: {
                title: 'Проекты | mirakzen'
            }
        },
        {
            path: '/games',
            name: 'GamesView',
            component: () => import('../views/Games.vue'),
            meta: {
                title: 'Игры | mirakzen'
            }
        },
        // {
        //     path: '/setup',
        //     name: 'SetupView',
        //     component: () => import('../views/Setup.vue'),
        //     meta: {
        //         title: 'Сэтап | mirakzen'
        //     }
        // },
        {
            path: "/:pathMatch(.*)*",
            name: 'ErrorView',
            component: () => import('../views/NotFound.vue'),
            meta: {
                title: 'mirakzen'
            }
        }
    ],
})

router.beforeEach((to, from, next) => {
    const title = to.meta.title
    if (title) {
        document.title = title
    }
    next()
})

export default router
