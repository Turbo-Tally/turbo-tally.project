import { createRouter, createWebHashHistory } from "vue-router";

import AccountSettingsPage from "@/pages/AccountSettingsPage.vue"
import CreatePollPage from "@/pages/CreatePollPage.vue"
import DashboardPage from "@/pages/DashboardPage.vue" 
import ForgotPasswordPage from "@/pages/ForgotPasswordPage.vue" 
import HomePage from "@/pages/HomePage.vue" 
import LogInPage from "@/pages/LogInPage.vue"
import PollResultsPage from "@/pages/PollResultsPage.vue" 
import PollsPage from "@/pages/PollsPage.vue" 
import SignUpPage from "@/pages/SignUpPage.vue"
import AnswerPollPage from "@/pages/AnswerPollPage.vue"

/**
 * Make router
 */
export function setupRouter () {
    const router = createRouter({
        history: createWebHashHistory(), 
        routes: defineRoutes() 
    }) 

    return router
}

/**
 * Define routes for the app
 */
function defineRoutes() {
    return [
        { path: "/", component: HomePage }, 
        { path: "/sign-up", component: SignUpPage }, 
        { path: "/log-in", component: LogInPage }, 
        { path: "/forgot-password", component: ForgotPasswordPage }, 
        { path: "/account", component: AccountSettingsPage },
        { path: "/dashboard", component: DashboardPage }, 
        { path: "/poll/create", component: CreatePollPage }, 
        { path: "/poll/:pollId/answer", component: AnswerPollPage }, 
        { path: "/polls", component: PollsPage },
        { path: "/polls/:pollId/report", component: PollResultsPage }
    ]
}