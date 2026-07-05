/**
 * Analytics composable for tracking page visits, facility views, and search queries.
 *
 * Usage:
 *   const analytics = useAnalytics()
 *   analytics.trackPageVisit('/')           // Track a page visit
 *   analytics.trackFacilityView(facility)   // Track a facility detail view
 *   analytics.trackSearchQuery(query, results, filters)  // Track a search
 */

interface AnalyticsPayload {
  path?: string
  referrer?: string
  user_agent?: string
  ip_hash?: string
  session_id?: string
  facility_id?: string
  facility_name?: string
  query_text?: string
  result_count?: number
  filters_applied?: Record<string, unknown>
}

const SESSION_ID_KEY = 'analytics_session_id'
const ANALYTICS_QUEUE_KEY = 'analytics_queue'

let analyticsBaseURL = ''
let sessionId = ''

const getSessionId = (): string => {
  if (!sessionId) {
    if (typeof window !== 'undefined') {
      sessionId = localStorage.getItem(SESSION_ID_KEY) || ''
      if (!sessionId) {
        sessionId = crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).slice(2)}`
        localStorage.setItem(SESSION_ID_KEY, sessionId)
      }
    }
  }
  return sessionId
}

const getQueue = (): AnalyticsPayload[] => {
  if (typeof window === 'undefined') return []
  try {
    const raw = localStorage.getItem(ANALYTICS_QUEUE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

const setQueue = (queue: AnalyticsPayload[]) => {
  if (typeof window === 'undefined') return
  localStorage.setItem(ANALYTICS_QUEUE_KEY, JSON.stringify(queue))
}

const flushQueue = async () => {
  if (typeof window === 'undefined') return
  const queue = getQueue()
  if (queue.length === 0) return

  const batch = [...queue]
  setQueue([]) // Clear queue optimistically

  for (const payload of batch) {
    let endpoint = ''
    if (payload.path !== undefined) {
      endpoint = `${analyticsBaseURL}/track/page-visit`
    } else if (payload.facility_id !== undefined) {
      endpoint = `${analyticsBaseURL}/track/facility-view`
    } else if (payload.query_text !== undefined) {
      endpoint = `${analyticsBaseURL}/track/search-query`
    }
    if (!endpoint) continue

    try {
      await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        // fire-and-forget with a short timeout
        signal: AbortSignal.timeout(5000),
      })
    } catch {
      // Re-queue failed payloads
      const currentQueue = getQueue()
      currentQueue.push(payload)
      setQueue(currentQueue)
      break // Stop processing on failure
    }
  }
}

const enqueue = (payload: AnalyticsPayload) => {
  if (typeof window === 'undefined') return
  const queue = getQueue()
  queue.push({
    ...payload,
    session_id: getSessionId(),
    user_agent: navigator.userAgent.substring(0, 500),
    referrer: payload.referrer ?? document.referrer.substring(0, 500),
  })
  setQueue(queue)

  // Flush asynchronously
  setTimeout(() => flushQueue(), 0)
}

let _initialized = false

const getApiURL = (): string => {
  if (typeof window === 'undefined') return ''
  try {
    const config = useRuntimeConfig()
    return config.public.apiURL || ''
  } catch {
    // Fallback for Options API components or non-setup context
    return (window as any).__NUXT__?.public?.apiURL || ''
  }
}

const initAnalytics = () => {
  if (_initialized || typeof window === 'undefined') return
  _initialized = true
  const apiURL = getApiURL()
  if (apiURL) {
    analyticsBaseURL = `${apiURL}/analytics`
  }
}

export const useAnalytics = () => {
  initAnalytics()

  /**
   * Track a page visit.
   * @param path - The URL path visited (e.g., '/', '/search', '/details')
   */
  const trackPageVisit = (path: string) => {
    enqueue({ path })
  }

  /**
   * Track a facility detail view.
   * @param facilityId - The ID of the facility being viewed
   * @param facilityName - Optional facility name for reporting
   */
  const trackFacilityView = (facilityId: string, facilityName?: string) => {
    enqueue({ facility_id: facilityId, facility_name: facilityName || '' })
  }

  /**
   * Track a search query.
   * @param queryText - The text the user searched for
   * @param resultCount - Number of results returned
   * @param filters - Any filters applied with the search
   */
  const trackSearchQuery = (queryText: string, resultCount: number = 0, filters?: Record<string, unknown>) => {
    enqueue({ query_text: queryText, result_count: resultCount, filters_applied: filters || {} })
  }

  /**
   * Manually flush the analytics queue (e.g., on page unload).
   */
  const flush = () => {
    // Use sendBeacon for reliability during page unload
    const queue = getQueue()
    if (queue.length === 0) return

    for (const payload of queue) {
      let endpoint = ''
      if (payload.path !== undefined) {
        endpoint = `${analyticsBaseURL}/track/page-visit`
      } else if (payload.facility_id !== undefined) {
        endpoint = `${analyticsBaseURL}/track/facility-view`
      } else if (payload.query_text !== undefined) {
        endpoint = `${analyticsBaseURL}/track/search-query`
      }
      if (!endpoint || typeof navigator === 'undefined' || !navigator.sendBeacon) continue

      navigator.sendBeacon(endpoint, JSON.stringify(payload))
    }
    setQueue([])
  }

  return {
    trackPageVisit,
    trackFacilityView,
    trackSearchQuery,
    flush,
  }
}
