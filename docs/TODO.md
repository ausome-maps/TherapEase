# TherapEase Development Roadmap

> Generated from open GitHub issues (#20–#94) and current repository state as of June 2026.
> Issues are triaged against the existing codebase to identify what is done, partially done, or not started.

---

## Project Milestones

| # | Milestone | Due | Progress | Status |
|---|---|---|---|---|
| 1 | **TherapEase 1st Deployment** | Aug 4, 2023 | 13/15 closed (86%) | Overdue — 2 issues remain |
| 2 | **TherapEase 2nd Deployment / UAT** | Aug 18, 2023 | 0/3 closed (0%) | Overdue — not started |

---

## 1. TherapEase 1st Deployment Milestone

**Goal:** Working Search page, Working Details page, complete data model, documented deployment workflow, documented data pipeline.

### 1.1 Feature: Search Page — Filter [#46](https://github.com/ausome-maps/TherapEase/issues/46)

- **Labels:** `feature`
- **Assignee:** Chibogret
- **Current state:** A filter component exists at `client/components/Search/AppFilter.vue` with basic capability (services_offered, caters_to checkboxes, region select, search text input). The search API endpoint (`POST /facilities/search`) already supports filtering by `services_offered` and free-text query via `django-opensearch-dsl`.
- **Remaining work:**
  1. Verify the existing `AppFilter.vue` fully satisfies the search page filter requirements (the issue lacks a description, so we assume the basic filter UI is what was intended).
  2. Add additional filter dimensions if missing: city, accreditation status (PAOT/PASP), contact availability.
  3. Ensure the filter state is preserved across page navigations and shared between the map view and the list view.
  4. Add URL query parameter sync for filter state (so filtered results can be bookmarked/shared).
  5. Mobile-responsive filter panel (collapsible drawer/sheet on small screens).
- **Estimated effort:** 3–5 days
- **Dependencies:** None (API supports filtering already)

### 1.2 Feature: Cards Component [#27](https://github.com/ausome-maps/TherapEase/issues/27)

- **Labels:** `feature`
- **Assignee:** Chibogret
- **User Story:** As a parent, I want to quickly see an overview of therapy centers/schools based on my search query.
- **Acceptance Criteria:** A reusable card component that displays a quick view of resulting facilities.
- **Current state:** A card component already exists at `client/components/Search/AppCard.vue` with `AppCardList.vue` as the container. It renders facility name, address, services offered badges, contact info, and a link to the details page. Cards are used in both the home page (`index.vue`) and search results page (`search-page.vue`).
- **Remaining work:**
  1. Audit the card component for completeness against the data model (`docs/data_model.md`): ensure all relevant fields are shown (accreditation badges via `AppAccBadge.vue`, operating hours if available, distance indicator).
  2. Add loading skeleton states for when facilities are being fetched.
  3. Add empty/error states for the card list.
  4. Ensure the component is properly registered for Nuxt auto-import (verify no manual import needed).
  5. Accessibility audit: ensure cards are keyboard-navigable and have proper ARIA labels.
- **Estimated effort:** 1–2 days
- **Status:** Likely closable after verification; mark as done if acceptance criteria are met.

---

## 2. TherapEase 2nd Deployment / UAT Milestone

**Goal:** P2P routing, built-in data form submission, OSM-TherapEase DB connection.

### 2.1 Feature: Design P2P Routing Interaction [#25](https://github.com/ausome-maps/TherapEase/issues/25)

- **Labels:** `design`
- **Description:** Create a Figma prototype for the P2P (person-to-person?) routing interaction.
- **Current state:** No Figma prototype exists in the repo. The `docs/interface_design.md` references existing Figma mockups but does not include a P2P routing design. The app currently shows facility locations on a Leaflet map (`AppMap.vue` / `AppDetailsMap.vue`) but has no routing/directions functionality.
- **Remaining work:**
  1. **Design phase:** Create a Figma prototype showing the user flow for getting directions from a user's current location to a selected facility. Consider: origin input (current location / manual address), route display on map, turn-by-turn instructions panel, mode of transport selector (driving, walking, transit).
  2. **Technical research:** Evaluate routing service options — OSRM (Open Source Routing Machine, self-hosted), GraphHopper, Mapbox Directions API, or Google Maps Directions API. Consider the Philippines-specific context and OSM data quality.
  3. Document the chosen routing approach (API integration spec, tile hosting if self-hosted).
- **Estimated effort:** Design: 3–5 days. Implementation: 5–10 days (future issue).
- **Dependencies:** Leaflet map already in place; needs routing library selection.

### 2.2 Task: Deployment for UAT [#22](https://github.com/ausome-maps/TherapEase/issues/22)

- **Labels:** `task`
- **Assignee:** lkpanganiban
- **Description:** No description provided beyond the title. This is the UAT (User Acceptance Testing) environment deployment.
- **Current state:** The repo has Ansible playbooks at `infrastructure/ansible/playbooks/` (provision.yml, update.yml, stop.yml) and Traefik configs for both dev and prod. Dockerfiles exist for both `api` and `client` in dev and prod variants. CI pipelines (GitHub Actions) build Docker images on push to `main`. However, there is no evidence of an actual UAT deployment being provisioned.
- **Remaining work:**
  1. **Provision UAT server:** Use the existing Ansible `provision.yml` playbook to set up a UAT server. Ensure `infrastructure/ansible/hosts.yml` has the UAT host configured.
  2. **Configure UAT-specific env vars:** Create a UAT variant of the `.env` file with UAT-specific settings (separate DB, separate MinIO bucket, SendGrid sandbox mode, reduced logging).
  3. **Set up UAT CI/CD:** Extend `.github/workflows/api-ci.yml` and `ui-ci.yml` to also deploy to the UAT server on merge/PR to a `uat` branch.
  4. **DNS/domain:** Configure a UAT subdomain (e.g., `uat.therapease.ph`) and point it to the UAT server.
  5. **SSL:** Ensure Traefik obtains Let's Encrypt certificates for the UAT domain.
  6. **Seed data:** Ensure the UAT instance has realistic test data (use `utils/load_data.py` against the UAT API).
  7. **Smoke tests:** Write a basic health-check script that hits key endpoints and verifies the UAT deployment.
- **Estimated effort:** 3–5 days
- **Dependencies:** Server access, domain/DNS configuration, API keys for external services.

### 2.3 (Implicit) OSM–TherapEase DB Connection

The milestone description mentions "OSM-TherapEase DB connection." There is no dedicated issue for this.

- **Current state:** The `docs/Map_Roulette_Adding_therapy_centers_challenge.md` documents a manual OSM mapping workflow. `utils/load_data.py` can bulk-load GeoJSON into the API. There is no automated sync between OSM and the TherapEase database.
- **Remaining work (if desired):**
  1. Design an OSM ingestion pipeline: periodic Overpass API queries for facilities matching certain tags (amenity=social_facility, healthcare=*, etc.) within the Philippines bounding box.
  2. Create a Celery periodic task to check for new/modified OSM nodes and insert/update them in the TherapEase DB.
  3. Handle deduplication (OSM node ID vs TherapEase facility UUID mapping).
- **Estimated effort:** 5–10 days (if pursued)
- **Note:** This is a large feature; may warrant its own milestone.

### 2.4 (Implicit) Built-in Data Form Submission

The milestone mentions "built-in data form submission." This overlaps with issue #90 (Self Service Facility Data Form). See section 4.3.

---

## 3. Un-Milestoned Issues — Backend

### 3.1 Integrate Social Media Authentication [#94](https://github.com/ausome-maps/TherapEase/issues/94)

- **Labels:** `backend`, `feature`
- **Description:** Enable users to sign in with Google and Facebook accounts instead of creating new platform-specific accounts.
- **Current state:** The backend has a `social_auth_jwt` view at `api/apps/core/users/social.py` that accepts `provider` (google-oauth2 / facebook) and `access_token`, uses `social_core` backends to authenticate, and returns JWT tokens. The frontend `useAuth.ts` composable has a `socialLogin()` method that posts to `/users/social/jwt/`. The URL route is defined in `api/apps/core/users/urls.py`.
- **Remaining work:**
  1. **Frontend OAuth UI:** Add "Continue with Google" and "Continue with Facebook" buttons on the login and registration pages (`pages/login.vue`, `pages/register.vue`). The current pages only have email/password forms.
  2. **OAuth token flow:** Implement the client-side OAuth flow using Google Identity Services (GIS) / Google OAuth 2.0 JS client or the Facebook JS SDK to obtain the `access_token` that gets passed to the backend.
  3. **Token refresh for social users:** Verify that JWT refresh works correctly for socially-authenticated users (they get the same token structure as email/password users, so this should already work, but test it).
  4. **Social profile linking:** Handle the case where a user signs up with email and later wants to link Google/Facebook (and vice versa). Currently not addressed.
  5. **Error handling:** Improve error messages on the frontend for social auth failures (e.g., "This Google account is not associated with a TherapEase account" vs network error).
  6. **Provider config in env:** Ensure Google OAuth client ID and Facebook App ID/secret are documented in `.env.sample` and configurable via environment variables.
- **Estimated effort:** 3–5 days
- **Dependencies:** Google Cloud Console project setup, Facebook App setup (admin tasks).

### 3.2 Facilities Workflow and Permissions [#87](https://github.com/ausome-maps/TherapEase/issues/87)

- **Labels:** `backend`, `feature`
- **Assignee:** lkpanganiban
- **Description:** Configure permissions for facility CRUD operations using the existing user and organization schemas. Users in organizations with the `manage_organization_facilities` permission should be able to manage facilities.
- **Current state:** A `FacilitiesPermissions` class exists at `api/apps/core/facilities/permissions.py`. It allows:
  - `list`, `retrieve`, `search` — public access.
  - `create`, `update`, `partial_update`, `destroy` — superusers, staff, or users with the `manage_organization_facilities` permission in an active `OrganizationRole`.
  - Object-level permission on update/delete checks the same conditions.
  - However, there is **no relationship between facilities and organizations** in the current `Facilities`/`FacilityProperties` model — the model has no `organization` ForeignKey field.
- **Remaining work:**
  1. **Add organization FK to Facility model:** Add `organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)` to `FacilityProperties` (or `Facilities`). Create and run the migration.
  2. **Scope facilities by organization:** Update the `FacilitiesPermissions` to enforce that a user can only create/update/delete facilities belonging to their own organization(s). Currently the permission just checks if the user *has* the role, not whether the facility belongs to their org.
  3. **Filter facilities by organization in API:** In the facility ViewSet, filter the queryset so that users only see facilities from their organization when performing mutating operations. For read-only operations (list/retrieve/search), all facilities remain public.
  4. **Auto-assign organization on create:** When a user creates a facility via the API, automatically assign it to the user's organization (or let them choose from orgs they belong to).
  5. **Admin panel support:** Update the Django admin for Facilities to show/edit the organization field.
  6. **Update frontend manage-facility page:** The `pages/manage-facility.vue` already exists and performs CRUD, but it does not consider organization context. Update it to show only the user's organization's facilities (and guard against cross-org access).
  7. **Update tests:** Extend `api/apps/core/facilities/tests.py` to cover org-scoped permission scenarios.
- **Estimated effort:** 5–7 days
- **Dependencies:** #89 (Registration flow — users need to be assigned to orgs) and #90 (Self-service facility form).

---

## 4. Un-Milestoned Issues — Interface/Frontend

### 4.1 Registration Flow [#89](https://github.com/ausome-maps/TherapEase/issues/89)

- **Labels:** `backend`, `feature`, `interface`
- **Status:** Linked to PR [#96](https://github.com/ausome-maps/TherapEase/pull/96)
- **Description:** Develop a registration form for providers (before expanding to public). Flow: (1) User enters email+password, (2) System sends confirmation email, (3) User clicks link, (4) User fills in remaining details (first_name, last_name, contact_nos, address, etc.), (5) User receives identity confirmation email. Non-activated accounts deleted after 1 day.
- **Sub-tasks:**
  - Registration API
  - Email Confirmation
  - Registration Form
  - Account Cleanup
- **Current state:** The backend uses Djoser for user registration (`POST /auth/users/`), activation (`POST /auth/users/activation/`), and email sending. Celery tasks in `api/apps/core/users/tasks.py` handle registration emails and account expiry checking (`check_expiry` — auto-deletes non-activated accounts after 1 day). The frontend has:
  - `pages/register.vue` — email + password registration form.
  - `pages/user/activate.vue` — activation page that takes `uid` and `token` from URL.
  - `pages/complete-profile.vue` — profile completion form after activation (first_name, last_name, other_metadata).
- **Remaining work:**
  1. **Audit the registration flow end-to-end:** Register a new user, check email delivery (or console email in dev), click activation link, complete profile. Identify any broken links or UX friction points.
  2. **Frontend redirection flow:** After registration, the user should be redirected to a "Check your email" page. After activation, redirect to the complete-profile page. After profile completion, redirect to the home page. Test this chain.
  3. **Provider-specific registration fields:** The current `complete-profile.vue` collects `first_name`, `last_name`, and `other_metadata`. Consider adding fields specific to providers: organization name (or org selection), professional credentials, facility association.
  4. **Error message improvements:** Ensure registration errors (duplicate email, weak password, etc.) are displayed clearly on the frontend.
  5. **Account cleanup Celery beat schedule:** Verify the `check_expiry` task is scheduled in `api/django_app/celery.py` and runs periodically.
  6. **Email template:** Review the registration email template used by Djoser. Customize it with TherapEase branding.
  7. **Referenced issue #85:** The issue references #85 (email service provider update) as a dependency. Verify SendGrid integration is configured in `django_app/settings.py` and that emails actually deliver in production/staging.
- **Estimated effort:** 2–3 days (mostly QA and polish)
- **Dependencies:** SendGrid API key (issue #85).

### 4.2 Self Service Facility Data Form [#90](https://github.com/ausome-maps/TherapEase/issues/90)

- **Labels:** `backend`, `feature`, `interface`
- **Description:** After providers are onboarded (registered, confirmed, assigned to an organization), they can create and modify facility information. Facilities belong to their organization. Users are manually assigned to organizations by TherapEase staff.
- **Current state:** The frontend has `pages/manage-facility.vue` which is a comprehensive form for creating/editing facilities. It handles all fields from the data model: basic info, contact info, accreditation, services offered (with mode selection), and coordinates. The backend has full CRUD endpoints at `/api/facilities/`. However, there is no organization-to-facility link in the model and no organization-based scoping in the form.
- **Remaining work:**
  1. **Organization-facility model link:** Add `organization` FK to the facility model (same task as issue #87, section 3.2).
  2. **Organization assignment UI:** Create an admin interface (Django admin page or a staff-only frontend page) where TherapEase staff can assign users to organizations with specific roles.
  3. **Update manage-facility form:** After the org-facility link exists, update `manage-facility.vue` to:
     - Show which organization the facility belongs to.
     - Pre-filter the facility list to show only the current user's organization's facilities.
     - Allow superusers/staff to select which organization a new facility belongs to.
  4. **"My Facilities" dashboard:** Create a page that lists all facilities belonging to the user's organization with edit/delete actions.
  5. **Submission workflow:** Consider adding a moderation/review step — when a provider creates/edits a facility, it goes into a "pending review" status before being published. This prevents bad data from reaching the public map.
  6. **Image upload:** The current form does not support image upload. Extend it to allow uploading facility photos to MinIO via the backend.
  7. **Validation:** Add client-side validation for required fields (placename) and coordinate bounds (must be within Philippines).
- **Estimated effort:** 5–8 days
- **Dependencies:** #87 (Facilities workflow/permissions), #89 (Registration flow).

### 4.3 Handle Mobile Support for Search and Detail Pages [#84](https://github.com/ausome-maps/TherapEase/issues/84)

- **Labels:** `feature`, `interface`
- **Description:** The search and detail pages need proper mobile/tablet responsive support. Proposal: tabbed view with map-centric and facilities list tabs.
- **Current state:** The home page (`pages/index.vue`) already has a mobile tab switcher (Facilities / Map tabs) implemented. It uses a `mobileTab` ref and shows/hides sections accordingly. Tailwind CSS v4 is used with responsive utility classes (`sm:`, `md:`, `lg:`). The search page (`pages/search-page.vue`) and details page (`pages/details-page.vue`) also exist but need a mobile audit.
- **Remaining work:**
  1. **Audit details page on mobile:** The `pages/details-page.vue` and its sub-components (`components/Details/AppContacts.vue`, `AppDetails.vue`, `AppFeatures.vue`, `AppGallery.vue`, `AppGalleryMobile.vue`, `AppDetailsMap.vue`) need testing on small viewports (320px–480px width). Check for overflow, touch target sizes (min 44px), and readability.
  2. **Audit search page on mobile:** `pages/search-page.vue` should be tested on mobile. Ensure the filter panel is usable (consider a slide-out drawer or modal for filters on mobile).
  3. **Shared components:** Audit `AppHeader.vue`, `AppFooter.vue`, `AppPagination.vue`, `AppSearchAndFilter.vue` for mobile usability.
  4. **Map interaction on touch devices:** Test pinch-to-zoom, tap-to-select markers, and scrolling behavior on the Leaflet map. The map should not capture scroll events when the user intends to scroll the page.
  5. **Detail page image gallery:** The `AppGalleryMobile.vue` component exists specifically for mobile — verify it works correctly and replaces the desktop gallery on small screens.
  6. **Performance:** Check that the mobile experience is performant (reduce initial map tile loading, lazy-load images, minimize JS bundle).
  7. **PWA consideration:** If we want offline capability, consider adding a service worker and a web app manifest for "Add to Home Screen" support on mobile.
- **Estimated effort:** 3–5 days
- **Dependencies:** None directly, but overlaps with #88 (mobile client).

### 4.4 TherapEase Mobile Client [#88](https://github.com/ausome-maps/TherapEase/issues/88)

- **Labels:** `feature`, `interface`
- **Description:** Build a dedicated mobile app (Android) using NativeScript-Vue. POC: replicate the existing web client into a mobile client.
- **Current state:** No mobile app code exists in the repository. This is a greenfield project. The web app is a Nuxt 4 SPA in `client/`.
- **Remaining work:** This is a large feature. A detailed plan:
  1. **Technology evaluation:**
     - **NativeScript-Vue** (mentioned in the issue): Allows building native Android/iOS apps with Vue. Pros: code reuse with existing Vue components. Cons: smaller ecosystem, requires native build tooling.
     - **Alternative — PWA:** Since the web app already uses responsive design, a PWA (Progressive Web App) could provide an "app-like" experience without a separate codebase. This would be far less effort.
     - **Alternative — Capacitor/Ionic:** Wraps the existing web app in a native shell. Better ecosystem than NativeScript.
     - **Recommendation:** Start with PWA + improved mobile web responsiveness (#84) first. If native features are needed (push notifications, offline storage), evaluate Capacitor.
  2. **If NativeScript is pursued:**
     - Set up a new `mobile/` directory in the monorepo with NativeScript project scaffolding.
     - Replicate auth flow (JWT login, token storage) using NativeScript HTTP and secure storage modules.
     - Replicate search page (list view with filters, map view using a NativeScript map plugin).
     - Replicate detail page with image gallery.
     - Implement deep linking for activation emails.
  3. **Shared code extraction:** Extract shared TypeScript logic (API client, auth composable, types/interfaces) into a shared package that both the web and mobile clients can consume.
- **Estimated effort:** PWA: 2–3 days. Native mobile app: 20–40 days (full POC).
- **Dependencies:** #84 (mobile web responsiveness) should be addressed first.

---

## 5. Un-Milestoned Issues — DevOps / QA

### 5.1 Setup Client Testing Framework [#91](https://github.com/ausome-maps/TherapEase/issues/91)

- **Labels:** `interface`
- **Description:** The frontend has no testing framework. Need to configure one and integrate it into the CI pipeline.
- **Current state:** There are zero test files in the `client/` directory (no `*.test.ts`, `*.spec.ts`, `__tests__/` directories). The `README.md` explicitly states "TODO: Setup a testing framework for the frontend." The CI (`ui-ci.yml`) only builds a Docker image.
- **Remaining work:**
  1. **Choose a testing framework:** For a Nuxt 4 / Vue 3 project, the community standard is **Vitest** (unit tests) + **@nuxt/test-utils** (component/integration tests with Nuxt context). For E2E testing, **Playwright** or **Cypress**.
  2. **Install and configure:**
     ```bash
     cd client
     npm install -D vitest @nuxt/test-utils @vue/test-utils happy-dom
     npx vitest init
     ```
  3. **Write example tests:**
     - **Unit test:** Test the `useAuth` composable in isolation (mock fetch, verify localStorage interactions, test login/logout/refresh flow).
     - **Component test:** Test `AppCard.vue` — mount with mock facility data, verify rendered fields, test click emits.
     - **Integration test:** Test the `pages/login.vue` — mount with Nuxt test utils, fill form, mock API response, verify redirect.
  4. **Configure coverage reporting:** Add `@vitest/coverage-v8` and set coverage thresholds.
  5. **Integrate with CI:** Update `.github/workflows/ui-ci.yml` to run `npm run test` (with a `"test": "vitest run"` script in `package.json`) before the Docker build step.
  6. **Add test scripts to package.json:**
     ```json
     "test": "vitest run",
     "test:watch": "vitest",
     "test:coverage": "vitest run --coverage"
     ```
  7. **Documentation:** Add a testing guide to `client/README.md` explaining how to write and run tests.
- **Estimated effort:** 3–5 days
- **Dependencies:** None

### 5.2 Setup Project Repository [#20](https://github.com/ausome-maps/TherapEase/issues/20)

- **Labels:** `task`
- **Description:** Setup project repository (GitHub/GitLab) with milestones, tasks, and subtasks.
- **Current state:** The repository exists on GitHub at `ausome-maps/TherapEase` with 14 issues, 2 milestones, and CI workflows. The milestones are overdue and incomplete.
- **Remaining work:**
  1. **Reorganize milestones:** Update milestone dates to be realistic. The current dates (Aug 2023) are 2+ years past due.
  2. **Create a 3rd milestone** for post-UAT features (mobile client, testing framework, social auth).
  3. **Assign issues to milestones:** Move un-milestoned issues (#84, #87, #88, #89, #90, #91, #94) into appropriate milestones.
  4. **Close completed issues:** Issues that are functionally done (especially #27 Cards component, #94 Social auth backend) should be verified and closed.
  5. **Create GitHub Projects board:** Set up a Kanban-style project board to track issue status visually.
  6. **Issue templates:** Add `.github/ISSUE_TEMPLATE/` with templates for bug reports, feature requests, and tasks.
- **Estimated effort:** 1–2 days (project management)

---

## 6. Additional Improvements (Not from Issues)

These are improvements identified during the repository review that are not covered by existing GitHub issues.

### 6.1 Frontend State Management

- **Current state:** No state management library (Vuex/Pinia) is used. Auth state lives in a reactive composable (`useAuth.ts`). Search/filter state is local to page components.
- **Recommendation:** Adopt **Pinia** for shared state management, especially as the app grows with organization context, user roles, and multi-page filter state. This would resolve prop-drilling and make state persistent across route navigations.

### 6.2 Backend API Documentation

- **Current state:** Swagger docs are available at `/docs/` via `drf-yasg`. However, the docs may not be fully up-to-date with all endpoints.
- **Recommendation:** Audit the Swagger schema, add docstrings to all viewsets, ensure request/response schemas are accurate. Consider migrating from `drf-yasg` (which is in maintenance mode) to `drf-spectacular` for OpenAPI 3.0 support.

### 6.3 Data Loading and Seed Data

- **Current state:** `utils/load_data.py` and `utils/load_images_to_bucket.py` exist but are noted as potentially outdated in the README.
- **Recommendation:** Audit the utility scripts, update them for the current API schema, and add them to the CI pipeline for seeding the UAT environment. Consider creating a Django management command (`python manage.py seed_data`) as an alternative.

### 6.4 Error Monitoring

- **Current state:** API logging is JSON-formatted (`django_app/log_formatter.py`). No error monitoring service (Sentry, etc.) is configured.
- **Recommendation:** Integrate Sentry SDK for both the Django backend and the Nuxt frontend to capture production errors.

### 6.5 Security Audit

- **Current state:** JWT tokens are stored in localStorage (vulnerable to XSS). CORS is configured. Environment variables use `.env`.
- **Recommendation:** Review security posture:
  - Consider httpOnly cookies for JWT storage (more secure but requires backend changes).
  - Add Content Security Policy headers.
  - Enable Django's `SECURE_*` settings in production (HSTS, secure cookies, etc.).
  - Add rate limiting to auth endpoints (Djoser supports throttling).
  - Run `pip-audit` or `safety` to check for known vulnerabilities in Python dependencies.
  - Run `npm audit` for frontend dependency vulnerabilities.

### 6.6 Internationalization (i18n)

- **Current state:** The app is English-only. The target audience is in the Philippines where Filipino/Tagalog and regional languages are widely spoken.
- **Recommendation:** Consider i18n support. Nuxt 4 has `@nuxtjs/i18n` module. For the backend, Django has built-in i18n with `gettext`. Start with Filipino translation as a secondary locale.

### 6.7 Analytics

- **Current state:** Google Tag Manager ID is in `.env.sample` (`GTM_ID`), suggesting analytics integration was planned but the implementation status is unclear.
- **Recommendation:** Verify GTM/GA integration on the frontend. Add event tracking for key user actions: search performed, facility viewed, registration started/completed, social login used.

---

## Priority Summary

| Priority | Issue | Description | Est. Effort |
|---|---|---|---|
| 🔴 P0 | #91 | Client testing framework | 3–5 days |
| 🔴 P0 | #87 | Facilities workflow & permissions | 5–7 days |
| 🔴 P0 | #22 | UAT deployment | 3–5 days |
| 🟡 P1 | #89 | Registration flow (QA & polish) | 2–3 days |
| 🟡 P1 | #90 | Self-service facility form | 5–8 days |
| 🟡 P1 | #84 | Mobile support for search/detail | 3–5 days |
| 🟡 P1 | #94 | Social auth (frontend buttons) | 3–5 days |
| 🟢 P2 | #20 | Repository organization | 1–2 days |
| 🟢 P2 | #46 | Search filter enhancements | 3–5 days |
| 🟢 P2 | #27 | Cards component audit/close | 1–2 days |
| 🟢 P2 | #25 | P2P routing design (Figma) | 3–5 days |
| 🟣 P3 | #88 | Mobile client (native app) | 20–40 days |
| 🟣 P3 | — | Pinia state management | 2–3 days |
| 🟣 P3 | — | API docs audit | 1–2 days |
| 🟣 P3 | — | Error monitoring (Sentry) | 1–2 days |
| 🟣 P3 | — | Security audit | 2–3 days |
| 🟣 P3 | — | i18n support | 3–5 days |
| 🟣 P3 | — | Analytics integration | 1–2 days |

---

## How to Use This Document

- Each section links to the corresponding GitHub issue.
- "Current state" describes what already exists in the codebase.
- "Remaining work" lists actionable, specific tasks.
- "Estimated effort" is in developer-days and should be refined by the team.
- This TODO.md should be updated whenever an issue is closed or a new feature is identified.
- After closing an issue, move it to a "Completed" section at the bottom of this document with a completion date.
