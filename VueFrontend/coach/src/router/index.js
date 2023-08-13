import { createRouter, createWebHistory } from "vue-router";
import CoachSignUp from "../views/coach/CoachSignUp.vue";
import ClientSignUp from "../views/client/ClientSignUp.vue";
import Dashboard from "../views/dashboard/Dashboard.vue";
import TweetDetail from "../views/dashboard/TweetDetail.vue";
import AddTweet from "../views/dashboard/AddTweet.vue";
import MyUserProfile from "../views/dashboard/MyUserProfile.vue";
import UserProfile from "../views/dashboard/UserProfile.vue";
import ForgotPassword from "../views/ForgotPassword.vue";
import ResetPassword from "../views/ResetPassword.vue";
import ConfirmAccount from "../views/ConfirmAccount.vue";


import EditUserProfile from "../views/dashboard/EditUserProfile.vue";
import store from "../store"
import Login from "../views/Login.vue";

const routes = [
  {
    path: "/coach-signup",
    name: "coach-signup",
    component: CoachSignUp,
  },
  {
    path: "/client-signup",
    name: "client-signup",
    component: ClientSignUp,
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard,
  },
  {
    path: "/forgot-password",
    name: "forgot-password",
    component: ForgotPassword,
  },
  {
    path: "/reset-password/:uid/:token",
    name: "reset-password",
    component: ResetPassword,
  },
  {
    path: "/dashboard/my-user-profile",
    name: "my-user-profile",
    component: MyUserProfile,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/tweet/:id',
    name: 'TweetDetail',
    component: TweetDetail,
  },
  {
    path: '/dashboard/add-tweet/',
    name: 'AddTweet',
    component: AddTweet,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/user-profile/:id',
    name: 'UserProfile',
    component: UserProfile,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-user-profile/edit/:id',
    name: 'EditUserProfile',
    component: EditUserProfile,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/confirmation/:token',
    name: 'ConfirmAccount',
    component: ConfirmAccount,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// proveravamo da li u state ima isAuthenticated i da li je required login i onda ako nije tacno
// saljemo ga na login
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router;
