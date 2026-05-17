## ⚠️ Important Notice

**Platform Interface Updates**

The deployment platforms referenced in this documentation (Render, Cloudflare Pages, GitHub) are third-party services that undergo frequent interface updates, feature additions, and workflow changes.

While the core concepts and configuration steps outlined in this guide remain valid, you may encounter minor differences in:

- Button labels and menu locations
- Visual layout and design
- Additional configuration options
- Terminology used in the platform UI

**What to do if you see differences:**

1. **Focus on the concept**, not the exact button position (e.g., "create a web service" vs. "deploy application")
2. **Look for equivalent fields** (e.g., "Build command" might be labeled "Build script")
3. **Consult the platform's official documentation** if a step seems unclear
4. **Contact support** if you encounter blocking issues

The fundamental deployment workflow (connect repo → configure build → set environment variables → deploy) remains consistent across platform updates.

_Last updated: May 2026_

---

## Backend Deployment on Render

### 1. Prerequisites

- GitHub account with access to the template repository
- Stable internet connection

### 2. Create a Render Account

1. Go to [render.com](https://render.com)
2. Click **Sign Up**
3. Authorize the connection with your GitHub account
4. Complete registration using your personal or professional email

### 3. Create a New Web Service

1. In the Render dashboard, click **New +** → **Web Service**
2. Connect to GitHub:
   - Select **GitHub** as the provider
   - Select where to install Render on your GitHub
   - Choose **Only select repositories** (recommended for security)
   - Check only the template repository
   - Click **Install** and confirm access

### 4. Configure the Service

Fill in the form as follows:

| Field              | Value                                        | Note                                                       |
| ------------------ | -------------------------------------------- | ---------------------------------------------------------- |
| **Name**           | `poc-template-3tier-api` (or preferred name) | Service identifier in dashboard                            |
| **Language**       | `Python 3`                                   | Native runtime (more stable)                               |
| **Branch**         | `main`                                       | Production branch                                          |
| **Region**         | `Frankfurt (EU Central)`                     | Lower latency for Brazil-based users                       |
| **Root Directory** | `backend`                                    | **Critical**: base folder for monorepo build and execution |

> Render will auto-detect `requirements.txt` and populate the build/start commands. Verify under **Advanced** if needed, but manual changes are typically unnecessary.

### 5. Select Plan

- **Instance Type**: `Free` ($0/month)
  - 512 MB RAM, 0.1 CPU
  - Ideal for PoC and demonstrations
  - Upgrade available anytime via dashboard

### 6. Configure Environment Variables

Under **Environment Variables**, add:

| Name              | Value                                               |
| ----------------- | --------------------------------------------------- |
| `APP_ENV`         | `production`                                        |
| `ALLOWED_ORIGINS` | `["http://localhost:3000","http://localhost:5173"]` |

> **Note**: The frontend URL will be added here after deploying the frontend. For now, keep only localhost entries.

### 7. Deploy

1. Click **Deploy Web Service**
2. Monitor progress under the **Logs** tab
3. Wait for status to change to **Live** (~2-4 minutes)

### 8. Validate Deployment

1. Copy the generated URL (e.g., `https://poc-template-3tier-api.onrender.com`)
2. Visit `https://<your-url>/docs` to open Swagger UI
3. Test available endpoints
4. Confirm `200 OK` responses

---

### ✅ Validation Checklist

- [ ] Service created with **Live** status
- [ ] Swagger UI accessible at `/docs`
- [ ] `/health` endpoint returns `200 OK`
- [ ] Environment variables configured correctly

### ⚠️ Expected Behaviors (Free Tier)

- **Cold start**: First request after inactivity may take 30-50 seconds
- **Volatile data**: In-memory database resets after sleep/redeploy
- **Auto-sleep**: Container pauses after ~15 minutes of inactivity

---

### 📋 Quick Reference (for consultation)

```
1. render.com → Sign Up with GitHub
2. New + → Web Service → GitHub → Select repo → Install
3. Config:
   - Name: poc-template-3tier-api
   - Language: Python 3
   - Branch: main
   - Region: Frankfurt
   - Root Directory: backend
   - Instance Type: Free
4. Environment Variables:
   - APP_ENV=production
   - ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
5. Create Web Service → Wait for Live status
6. Validate: https://<url>/docs
```

---

### ℹ️ Additional Notes

- **In-memory database**: Data persists while the container is active. It is cleared only on redeploy or after auto-sleep (~15 min of inactivity). This is expected behavior for PoC environments.
- **CORS configuration**: Remember to update `ALLOWED_ORIGINS` with the Vercel frontend URL after completing the frontend deployment.
- **Logs & debugging**: Use the **Logs** tab in the Render dashboard for real-time output and error troubleshooting.

---

## Frontend Deployment on Cloudflare Pages

### 1. Prerequisites

- GitHub account with access to the template repository
- Backend API already deployed and accessible (e.g., on Render)
- Stable internet connection

### 2. Create a Cloudflare Account

1. Go to [pages.cloudflare.com](https://pages.cloudflare.com)
2. Click **Sign up with GitHub**
3. Authorize the connection with your GitHub account
4. Complete registration using your personal or professional email

### 3. Create a New Pages Project

1. In the Cloudflare Pages dashboard, click **Create application**
2. Select **Pages** → **Connect to Git**
   > ⚠️ Ensure you select **Pages**, not Workers. Workers are for backend scripts; Pages is for static sites/SPAs.
3. Connect to GitHub:
   - Choose **Only select repositories** (recommended for security)
   - Check only the template repository (e.g., `poc-template-3tier`)
   - Click **Install** and confirm access
4. Select the repository and click **Begin setup**

### 4. Configure the Build

Fill in the build settings as follows:

| Field                      | Value                                        | Note                               |
| -------------------------- | -------------------------------------------- | ---------------------------------- |
| **Project name**           | `poc-template-3tier-frontend` (or preferred) | Identifier in Cloudflare dashboard |
| **Production branch**      | `main`                                       | Branch to deploy from              |
| **Framework preset**       | `React (Vite)`                               | Auto-configures build commands     |
| **Build command**          | `npm run build`                              | Populated automatically by preset  |
| **Build output directory** | `dist`                                       | Populated automatically by preset  |

#### 🔽 Expand Advanced Settings

Click **`> Root directory (advanced)`** and set:
| Field | Value | Note |
|-------|-------|------|
| **Root directory** | `frontend` | **Critical**: Base folder for monorepo; ensures build runs inside `frontend/` |

### 5. Configure Environment Variables

Click **`> Environment variables (advanced)`** → **Add variable**:

| Variable name       | Variable value                            |
| ------------------- | ----------------------------------------- |
| `VITE_API_BASE_URL` | `https://<your-backend-url>.onrender.com` |

> Replace `<your-backend-url>` with the actual URL of your deployed backend API (e.g., `poc-template-3tier-api`).

### 6. Deploy

1. Click **Save and Deploy**
2. Monitor progress under the **Deployments** tab
3. Wait for status to change to **Success** (~1-2 minutes)
4. Copy the generated URL (e.g., `https://<project-id>.poc-template-3tier.pages.dev`)

### 7. Update Backend CORS (Critical)

After obtaining the frontend URL:

1. Go to your backend service dashboard (e.g., Render)
2. Navigate to **Environment Variables**
3. Update `ALLOWED_ORIGINS` to include the new frontend URL:
   ```json
   [
     "https://<your-frontend-url>.pages.dev",
     "http://localhost:3000",
     "http://localhost:5173"
   ]
   ```
4. Save changes → backend will redeploy automatically (~1 min)

### 8. Validate Deployment

1. Access the frontend URL in your browser
2. Navigate between pages (e.g., Items, Not Found)
3. Open DevTools → **Network** tab → confirm API calls return `200 OK`
4. Verify no CORS errors appear in the console

---

### ✅ Validation Checklist

- [ ] Deployment status shows **Success**
- [ ] Frontend loads without blank screen or 404 errors
- [ ] Navigation between routes works (React Router handling)
- [ ] API calls succeed (`200 OK` in Network tab)
- [ ] No CORS errors in browser console
- [ ] Backend `ALLOWED_ORIGINS` includes the frontend URL

### ⚠️ Expected Behaviors (Free Tier)

- **Cold start (backend)**: First API request after backend inactivity may take 30-50 seconds
- **SPA routing**: All routes are handled client-side; direct links to sub-pages work after initial load
- **Build caching**: Subsequent deploys are faster due to cached `node_modules`

---

### 📋 Quick Reference (for consultation)

```
1. pages.cloudflare.com → Sign up with GitHub
2. Create application → Pages → Connect to Git
3. Select repo → Begin setup
4. Config:
   - Framework preset: React (Vite)
   - Root directory: frontend
   - Build command: npm run build
   - Output directory: dist
5. Environment Variables:
   - VITE_API_BASE_URL=https://<backend-url>.onrender.com
6. Save and Deploy → Wait for Success
7. Update backend CORS with new frontend URL
8. Validate: https://<url>.pages.dev
```

---

### ℹ️ Additional Notes

- **Monorepo support**: The `Root directory: frontend` setting ensures Cloudflare executes all commands relative to the `frontend/` folder, isolating it from the backend code.
- **SPA routing**: Cloudflare Pages handles client-side routing automatically for Vite/React projects. No additional configuration is required.
- **Custom domain**: You can add a custom domain later via **Custom domains** in the Cloudflare Pages dashboard (free with SSL).
- **Rollback**: Previous successful deployments are retained. Rollback via **Deployments** → select version → **Rollback to this deployment**.

---

## 🌐 Reference Demo

Want to see a working example before deploying? Check our live demo:

- Frontend: https://b49c5e3f.poc-template-3tier.pages.dev
- Backend: https://poc-template-3tier-api.onrender.com/docs

This helps you understand the expected behavior and performance of your own deployment.
