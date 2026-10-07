# AiInsight System Architecture

AutoML / AiInsight is a full-stack platform that performs automated Exploratory Data Analysis (EDA), model suggestion, and data visualization on uploaded CSVs.

## Directory Structure

```text
AiInsight/
├── backend/          # Flask application + ML pipeline (Python)
├── frontend/         # Vue 3 application + TailwindCSS (JS)
├── README.md         # Architecture overview (this file)
```

## System Flow

1. **Upload Phase**: A user (or public guest, if `allow_public_upload` is enabled) uploads a `.csv` dataset via `/api/dataset/csv`.
2. **Analysis Pipeline**: The backend (`AutoML` engine in `ml_services.py`) parses the dataset, handles missing data safely, calculates statistical distributions, and renders correlation/heatmap/histogram charts (base64 PNGs) using `matplotlib`.
3. **Model Strategy**: A rule-based suggestion engine infers whether the dataset requires Regression, Classification, or Clustering based on the target variable.
4. **Persistence**: The full payload (EDA metrics, charts, AI suggestions) is persisted to an SQLite database (which runs locally at `backend/instance/ai.db`) tied to the user's account.
5. **Dashboard Rendering**: The Vue frontend requests the `/api/user/eda` endpoint and maps the JSON response into interactive stat tiles and chart views on the unified `Reports` dashboard.

## Database & Models

We use `Flask-SQLAlchemy` wrapping `SQLite`.

- **Users**: Core identities, including the global `ADMIN` account (`username: skym1618`).
- **Dataset**: File manifest (`name`, `path`, `rows`, `columns`, `status`).
- **EDAReport**: Large JSON payload storing statistical facts about categorical/numeric columns.
- **Visualization**: Base64 encoded charts rendered specifically for a dataset.
- **AISuggestion**: Rule-based parameters (task type, model algo, hyper-parameters) proposed for the user's data.
- **SystemSettings**: Singleton row (id=1) where the Admin toggles global authentication and public upload rights.

## API Architecture

The backend exposes several Blueprints mounted under `/api/`:
- `/api/auth/` — JWT-based authentication (Login, Register).
- `/api/admin/` — Admin-only controls (Global toggles, user management, platform metrics).
- `/api/dataset/` — Uploads and file operations.
- `/api/user/` — Standard views (Overview statistics, EDA fetching, Dataset deletion) locked to the requesting user.
- `/api/ml/` — Internal tools to arbitrarily re-run the `AutoML` engine against an already-saved dataset.

*Note: All protected routes resolve the caller via `resolve_actor()`. The system can run in a "Demo Mode" where JWTs are ignored gracefully based on the dynamic `SystemSettings.auth_enabled` flag.*

## Frontend Stack & Routing

The frontend (`Vite` + `Vue3` + `TailwindCSS`) provides a clean, responsive SPA.

- **Axios Interceptors**: Automatically hook into local storage to append `Bearer [TOKEN]` headers to every dispatch, and capture `401 Unauthorized` responses to seamlessly route users back to login without flashing broken screens.
- **Vue Router**: Governed by a `beforeEach` navigation guard ensuring authenticated views stay protected, whilst simultaneously locking `/admin` endpoints away from standard `USER` roles.

## Running the Stack

- **Backend**: `python run.py` (Runs on `http://127.0.0.1:5000`)
- **Frontend**: `npm run dev` (Runs on Vite port, proxying `/api` traffic internally avoiding CORS issues on standard localports).
