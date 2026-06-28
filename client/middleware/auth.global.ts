export default defineNuxtRouteMiddleware(async (to) => {
  const protectedRoutes = ['/complete-profile', '/profile']
  const adminRoutes = ['/admin']
  const authPages = [
    '/login',
    '/register',
    '/complete-profile',
    '/user/activate',
    '/user/reset-password',
    '/profile',
    '/admin',
  ]

  if (import.meta.server) return

  const config = useRuntimeConfig()
  const authEnabled = config.public.authEnabled
  const registrationEnabled = config.public.registrationEnabled

  if (!authEnabled && authPages.some((p) => to.path.startsWith(p))) {
    return navigateTo('/')
  }

  if (!registrationEnabled && to.path.startsWith('/register')) {
    return navigateTo('/login?registrationDisabled=true')
  }

  const hasToken = !!localStorage.getItem('access_token')

  if (protectedRoutes.some((p) => to.path.startsWith(p)) && !hasToken) {
    return navigateTo('/login')
  }

  if (adminRoutes.some((p) => to.path.startsWith(p))) {
    if (!hasToken) return navigateTo('/login')
    const { initAuth, isStaff, isSuperuser } = useAuth()
    await initAuth()
    if (!isStaff.value && !isSuperuser.value) {
      return navigateTo('/')
    }
  }
})
