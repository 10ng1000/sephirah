const routes = [
  {
    path: "/",
    redirect: "/chat",
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
    path: "/knowledge",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/ShelfPage.vue") }],
  },
  {
    path: "/extract",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/ChatPage.vue") }],
  },
  {
    path: "/books/:book_id",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/BookPage.vue") }],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("../pages/ErrorNotFound.vue")
  }
]

export default routes
