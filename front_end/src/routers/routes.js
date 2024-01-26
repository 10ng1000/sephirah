const routes = [
  {
    path: "/",
    component: () => import("/src/layouts/MainLayout.vue"),
  },
  {
    path: "/chat/:session_id",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/ChatPage.vue") }],
  },
  {
    path: "/chat",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/ChatPage.vue") }],
  },
  {
    path: "/memory",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/MemoryBankPage.vue") }],
  },
  {
    path: "/graph",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/ChatPage.vue") }],
  },
  {
    path: "/knowledge",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/ChatPage.vue") }],
  },
  {
    path: "/extract",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/ChatPage.vue") }],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("../pages/ErrorNotFound.vue")
  }
]

export default routes
