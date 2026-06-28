# TherapEase Infrastructure

Ansible-based deployment for the TherapEase platform on a single Ubuntu server, orchestrated with Docker Compose and routed through Traefik with Let's Encrypt TLS.

## Directory Structure

```
infrastructure/
├── ansible/
│   ├── hosts.yml                         # Inventory — server IP, secrets, domain names
│   └── playbooks/
│       ├── provision.yml                 # First-time server setup + deploy
│       ├── update.yml                    # Redeploy latest images
│       ├── stop.yml                      # Stop all services
│       └── roles/
│           ├── base/
│           │   └── tasks/
│           │       ├── main.yml          # Locale, apps dir
│           │       └── docker.yml        # Install Docker + docker-compose
│           └── therapease-deployment/
│               ├── defaults/main.yml     # Variable fallback defaults
│               ├── tasks/
│               │   ├── main.yml          # Role entry point
│               │   ├── app.yml           # Create dirs, template configs, pull images
│               │   └── start.yml         # Stop then start Docker Compose
│               └── templates/
│                   ├── acme.json                    # LetsEncrypt state placeholder
│                   ├── docker-compose.therapease.prod.yml.j2  # Production compose file
│                   ├── docker.env.j2                # Environment variables
│                   ├── traefik.prod.toml            # Traefik static config
│                   └── traefik_dynamic.toml         # Traefik dynamic config (dashboard auth)
└── traefik/
    ├── Dockerfile              # Custom Traefik image (dev/local)
    ├── traefik.dev.toml        # Development Traefik config
    └── traefik.prod.toml       # Standalone production config (unused — Ansible template used instead)
```

## Prerequisites

### Local Machine (Operator)
- **Ansible** ≥ 2.9
  ```bash
  pip install ansible
  ```
- SSH access to the target server (key-based auth recommended)
- GitHub Container Registry credentials (Personal Access Token with `read:packages` scope)

### Target Server
- **Ubuntu 20.04 / 22.04** (other Debian-based distros may work)
- **Docker** — installed automatically by the `base` role
- **docker-compose** (Python package) — installed automatically
- Ports open: **80** (HTTP), **443** (HTTPS), **22** (SSH)
- A non-root user with `sudo` privileges (default: `therapease`)

### External Services
- **DNS**: A records for the domain names pointing to the server IP
  - `api.<domain>` → API
  - `<domain>` → Frontend UI
  - `storage.<domain>` → MinIO console
  - `s3.<domain>` → MinIO API
  - `monitor.<domain>` → Traefik dashboard
- **SendGrid**: API key for transactional emails (registration, submission notifications)
- **GitHub Container Registry**: `ghcr.io` — the API and UI Docker images are published here

## Configuration

### 1. Edit the Inventory

All server variables are in `ansible/hosts.yml`. Replace every `<placeholder>`:

```yaml
all:
  hosts: <ip-address>           # Server IP
  vars:
    ansible_port: 22
    ansible_user: therapease    # Server user with sudo
    cr:
      user: <github-username>   # GHCR username
      password: <github-pat>    # GHCR personal access token

    therapease_api_domain_name: "api.example.com"
    therapease_ui_domain_name: "example.com"
    therapease_storage_domain_name: "storage.example.com"
    therapease_api_storage_domain_name: "s3.example.com"
    therapease_monitor_domain_name: "monitor.example.com"
    sendgrid_api_key: "<sendgrid-api-key>"
    therapease_system_email: "noreply@example.com"   # Must be verified in SendGrid
    therapease_admin_email: "admin@example.com"
    api_secret_key: "<random-50-char-string>"
    geocode_url: "https://nominatim.openstreetmap.org/search"
    feedback_url: "https://forms.gle/Yo4zMgBXXfAL7vyS6"
    google_tag_manager: "https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"
    feature_auth_enabled: 1
    feature_registration_enabled: 0
    is_ssl: false  # Let's Encrypt configures TLS; this flag is reserved for future use
    minio:
      root: <minio-access-key>
      password: <minio-secret-key>
    postgres:
      username: <db-user>
      password: <db-password>
      host: therapease_db    # Docker service name — do not change
      dbname: therapeasedb
    deploy_therapease: yes
```

### 2. Environment Variables Reference

The `docker.env.j2` template renders these variables for all containers:

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | Required |
| `GEOCODE_URL` | Nominatim geocoding endpoint | `https://nominatim.openstreetmap.org/search` |
| `REDIS_URL` | Celery broker | `redis://therapease_cache:6379` |
| `REDIS_CACHED` | Django cache backend | `redis://therapease_cache:6379` |
| `NUXT_PUBLIC_API_URL` | API URL for frontend | `https://<api-domain>` |
| `NUXT_PUBLIC_UI_URL` | UI URL for frontend | `https://<ui-domain>` |
| `POSTGRES_USER/PASSWORD/DB/HOST/PORT` | Database connection | From `hosts.yml` |
| `DEBUG` | Django debug mode | `0` (always off in prod) |
| `FEATURE_AUTH_ENABLED` | Enable login/register | `1` |
| `FEATURE_REGISTRATION_ENABLED` | Enable new user registration | `0` |
| `MINIO_ROOT_USER/PASSWORD` | MinIO container credentials | From `hosts.yml` |
| `MINIO_ACCESS_KEY/SECRET_KEY` | MinIO S3 client credentials | Same as ROOT_USER/PASSWORD |
| `MINIO_ENDPOINT` | Internal MinIO endpoint | `therapease_storage:9000` |
| `MINIO_SECURE` | Use HTTPS for MinIO (0=off) | `0` (Traefik handles TLS) |
| `MINIO_BUCKET` | Bucket for submission images | `submissions` |
| `MINIO_PUBLIC_ENDPOINT` | Public MinIO URL | `https://<s3-domain>` |
| `SENDGRID_HOST_PASSWORD` | SendGrid API key | From `hosts.yml` |
| `DEFAULT_FROM_EMAIL` | System email sender | From `hosts.yml` |
| `ADMIN_EMAIL` | Admin email for notifications | From `hosts.yml` |

## Deployment

### First-Time Provisioning

Run from the `infrastructure/ansible` directory:

```bash
ansible-playbook -i hosts.yml playbooks/provision.yml --ask-become-pass
```

This will:
1. Set the system locale to `en_PH.UTF-8`
2. Install `ntp` and `htop`
3. Install Docker and docker-compose
4. Create data directories at `/datadrive/{postgres,storage,backups}`
5. Render and deploy all configuration files to `~/apps/`
6. Pull the latest API and UI Docker images from `ghcr.io`
7. Create the `acme.json` file for Let's Encrypt (mode `0600`)

### Update / Redeploy

After pushing new images to GHCR or changing configuration:

```bash
ansible-playbook -i hosts.yml playbooks/update.yml --ask-become-pass
```

This re-templates the compose file and `.env`, pulls the latest images, and restarts all services. It does **not** re-run the `base` role (no system package changes).

### Stop All Services

```bash
ansible-playbook -i hosts.yml playbooks/stop.yml --ask-become-pass
```

## Service Architecture

After deployment, `docker compose ps` will show:

| Container | Image | Internal Port | Public via Traefik | Notes |
|---|---|---|---|---|
| `traefik` | `traefik:v2.10.4` | 80, 443 | All domains | Reverse proxy + TLS |
| `therapease_frontend` | `ghcr.io/ausome-maps/therapease-ui:latest` | 9002 | `ui_domain_name` | Nuxt 4 SPA |
| `therapease_api` | `ghcr.io/ausome-maps/therapease-api:latest` | 9003 | `api_domain_name` | Django + Gunicorn |
| `therapease_storage` | `docker.io/bitnami/minio:2023` | 9000, 9001 | `storage_domain_name` + `s3_domain_name` | S3-compatible storage |
| `therapease_db` | `postgres:15.4-alpine3.18` | — | None | Internal only |
| `therapease_cache` | `redis:6.0.20-alpine3.18` | — | None | Internal only |

### Networks
- **web** (external): Shared between Traefik and app containers for routing
- **internal** (bridge): Private communication between API, DB, Cache, Storage

### Volumes
| Mount | Host Path | Container Purpose |
|---|---|---|
| `postgres_data` | `/datadrive/postgres` | PostgreSQL data |
| `minio_data` | `/datadrive/storage` | Uploaded images and files |
| `backup_data` | `/datadrive/backups` | Django DB backups |
| `acme.json` | `~/apps/traefik/acme.json` | Let's Encrypt certificates |

## Traefik Configuration

### Static Config (`traefik.prod.toml`)
- Entrypoints: `web` (HTTP → redirects to HTTPS), `websecure` (HTTPS)
- Docker provider with `watch = true` on the `web` network
- File provider for dynamic routes (dashboard auth)
- Let's Encrypt resolver with TLS challenge

### Dynamic Config (`traefik_dynamic.toml`)
- Exposes the Traefik dashboard at `monitor_domain_name` protected by basic auth
- Default credentials: `admin` (hashed with APR1)
- Change the password hash before deploying to production

### Changing the Dashboard Password

```bash
# Generate a new password hash
openssl passwd -apr1 "your-new-password"

# Replace the hash in traefik_dynamic.toml
```

## CI/CD Integration

The GitHub Actions workflows build and push Docker images to GHCR:

- `.github/workflows/api-ci.yml` — builds the API image on push/PR to `main`
- `.github/workflows/ui-ci.yml` — builds the UI image on push/PR to `main`

After CI pushes new images to GHCR, run the `update.yml` playbook to redeploy.

## Troubleshooting

### View logs
```bash
ssh therapease@<server>
cd ~/apps
docker compose -f docker-compose.therapease.yml logs -f --tail=100 <service>
```

### Check Traefik routing
```bash
# Dashboard (if monitor domain is configured)
curl -u admin:<password> https://monitor.example.com/api/rawdata

# Test API endpoint directly (bypassing Traefik)
curl http://localhost:9001/api/facilities/
```

### Certificate issues
```bash
# Check acme.json permissions
ls -la ~/apps/traefik/acme.json    # Should be -rw------- (600)

# Traefik certificate resolver logs
docker compose -f ~/apps/docker-compose.therapease.yml logs traefik | grep -i acme
```

### Database migration issues
The API container's entrypoint runs `python manage.py migrate` on startup. If migrations fail:

```bash
docker compose -f ~/apps/docker-compose.therapease.yml exec api python manage.py migrate --plan
docker compose -f ~/apps/docker-compose.therapease.yml exec api python manage.py showmigrations
```

### Redis / Celery issues
If notification emails aren't being sent:
```bash
# Check Redis connectivity from the API container
docker compose -f ~/apps/docker-compose.therapease.yml exec api python -c "import redis; r=redis.Redis(host='therapease_cache',port=6379); print(r.ping())"
```

Note: The API gracefully handles Redis/Celery being unavailable — submissions will still be saved, but notification emails will not be enqueued until Redis is back up.
