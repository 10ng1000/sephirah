const routes = [
  {
    path: "/",
    redirect: "/chat"
  },
  {
    path: "/chat",
    component: () => import("../layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("../pages/ChatPage.vue") }],
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
  // // Always leave this as last one,
  // // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("../pages/ErrorNotFound.vue")
  }
]

export default routes