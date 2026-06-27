export default defineNuxtRouteMiddleware((to) => {
  const protectedRoutes = ['/complete-profile']

  if (import.meta.server) return

  const hasToken = !!localStorage.getItem('access_token')

  if (protectedRoutes.includes(to.path) && !hasToken) {
    return navigateTo('/login')
  }
})
