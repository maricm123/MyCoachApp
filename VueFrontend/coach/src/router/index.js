import { createRouter, createWebHistory } from "vue-router";
import CoachSignUp from "../views/coach/CoachSignUp.vue";
import ClientSignUp from "../views/client/ClientSignUp.vue";
import Dashboard from "../views/dashboard/Dashboard.vue";
import TrainingDetail from "../views/dashboard/TrainingDetail.vue";
import TrainingDetail2 from "../views/dashboard/TrainingDetail2.vue";
import AddTrainingProgram from "../views/dashboard/AddTrainingProgram.vue";
import CreatePaymentMethod from "../views/client/CreatePaymentMethod";
import Subscription from "../views/subscription/Subscription.vue";
import Cancel from "../views/subscription/Cancel.vue";
import Success from "../views/subscription/Success.vue";
import ClientUserProfile from "../views/client/ClientUserProfile.vue";
import CoachUserProfile from "../views/coach/CoachUserProfile.vue";

import ClientPaymentMethods from '../views/client/ClientPaymentMethods.vue'
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
  // {
  //   path: "/reset-password/:uid/:token",
  //   name: "reset-password",
  //   component: ResetPassword,
  // },
  {
    path: "/dashboard/client-user-profile",
    name: "client-user-profile",
    component: ClientUserProfile,
    meta: {
      requireLogin: true
    }
  },
  {
    path: "/dashboard/coach-user-profile",
    name: "coach-user-profile",
    component: CoachUserProfile,
    meta: {
      requireLogin: true
    }
  },
  // {
  //   path: '/dashboard/training/:id',
  //   name: 'TrainingDetail',
  //   component: TrainingDetail,
  // },
  {
    path: '/dashboard/training/:id',
    name: 'TrainingDetail',
    component: TrainingDetail2,
  },
  {
    path: '/dashboard/subscribe',
    name: 'Subscription',
    component: Subscription,
  },
  {
    path: '/dashboard/subscribe/cancel',
    name: 'Cancel',
    component: Cancel,
  },
  {
    path: '/dashboard/subscribe/success',
    name: 'Success',
    component: Success,
  },
  {
    path: '/dashboard/add-training-program/',
    name: 'AddTrainingProgram',
    component: AddTrainingProgram,
    meta: {
      requireLogin: true
    }
  },
  {
    path: "/dashboard/client-user-profile/create-payment-method",
    name: "CreatePaymentMethod",
    component: CreatePaymentMethod,
    meta: {
      requireLogin: true
    }
  },
  {
    path: "/dashboard/client-user-profile/get-payment-methods",
    name: "ClientPaymentMethods",
    component: ClientPaymentMethods,
    meta: {
      requireLogin: true
    }
  },
  // {
  //   path: '/dashboard/user-profile/:id',
  //   name: 'UserProfile',
  //   component: UserProfile,
  //   meta: {
  //     requireLogin: true
  //   }
  // },
  // {
  //   path: '/dashboard/my-user-profile/edit/:id',
  //   name: 'EditUserProfile',
  //   component: EditUserProfile,
  //   meta: {
  //     requireLogin: true
  //   }
  // },
  // {
  //   path: '/confirmation/:token',
  //   name: 'ConfirmAccount',
  //   component: ConfirmAccount,
  // },
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
