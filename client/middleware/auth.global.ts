export default defineNuxtRouteMiddleware((to) => {
  const protectedRoutes = ['/complete-profile']
  const authPages = ['/login', '/register', '/complete-profile', '/user/activate', '/user/reset-password']

  if (import.meta.server) return

  const config = useRuntimeConfig()
  const authEnabled = config.public.authEnabled

  if (!authEnabled && authPages.some((p) => to.path.startsWith(p))) {
    return navigateTo('/')
  }

  const hasToken = !!localStorage.getItem('access_token')

  if (protectedRoutes.includes(to.path) && !hasToken) {
    return navigateTo('/login')
  }
})
