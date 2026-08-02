# ITSM GitHub Pages

Static recovery-era site from this `docs/` folder.

**Custom domain:** `itsm-cosmology.com` (see `CNAME`)

## Local preview

```powershell
cd docs
python -m http.server 8080
# http://localhost:8080
```

## Enable on GitHub

1. Repo **Settings → Pages**
2. Source: **GitHub Actions** (workflow `github-pages`) *or* branch `recovery/v12-core-architecture` → folder `/docs`
3. Under **Custom domain**, enter `itsm-cosmology.com` and save  
   (GitHub will use the `docs/CNAME` file after the next deploy)
4. Enable **Enforce HTTPS** once DNS has propagated and the certificate is ready

Site URLs:

- Custom: https://itsm-cosmology.com  
- Fallback: https://brendohxd.github.io/ITSM-Integrated-Toroidal-Syntropic-Model/

## DNS at your domain registrar (itsm-cosmology.com)

Point the domain at GitHub Pages. Use **one** of these setups.

### Option A — Apex only (`itsm-cosmology.com`)

| Type | Name / Host | Value |
|------|-------------|--------|
| **A** | `@` | `185.199.108.153` |
| **A** | `@` | `185.199.109.153` |
| **A** | `@` | `185.199.110.153` |
| **A** | `@` | `185.199.111.153` |
| **AAAA** (optional IPv6) | `@` | `2606:50c0:8000::153` |
| **AAAA** | `@` | `2606:50c0:8001::153` |
| **AAAA** | `@` | `2606:50c0:8002::153` |
| **AAAA** | `@` | `2606:50c0:8003::153` |

### Option B — Also serve `www.itsm-cosmology.com`

Add Option A, plus:

| Type | Name / Host | Value |
|------|-------------|--------|
| **CNAME** | `www` | `brendohxd.github.io` |

In GitHub Pages settings you can set the primary custom domain to `itsm-cosmology.com` and check “Redirect www → apex” if offered.

### If the registrar only allows CNAME on apex

Use their **ALIAS / ANAME / flattened CNAME** feature (Cloudflare “CNAME flattening”, etc.) pointing `@` → `brendohxd.github.io`.

## Relation to itsm-cosmology.org

`.com` can host this recovery research Pages site.  
`.org` can stay as the separate explorer/brand site if you want both. Avoid two sites contradicting claim hygiene — either align `.org` or link clearly.

## Content policy

Recovery claim hygiene only (master plan + selective publishing). No withdrawn packaging as live predictions.
