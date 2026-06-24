# Subscription Watchdog - Memory + MCP Server Layer (Member 3) 🚀

This is the **Memory + MCP Server layer** for the **Subscription Watchdog** project. It exposes an MCP (Model Context Protocol) server over **Streamable HTTP** that stores, retrieves, and flags recurring subscription charges in a hosted Neon PostgreSQL database.

---

## Technical Stack 🛠️

- **Language:** Python 3.11+
- **MCP Framework:** FastMCP (v2.x)
- **DB Driver:** psycopg2-binary
- **Database:** Neon PostgreSQL (hosted cloud database)
- **Transport:** Streamable HTTP (for remote connectivity over the web)

---

## Project Structure 📁

- `server.py`: FastMCP server containing tools: `add_sub`, `get_subs`, and `flag_sub`.
- `db.py`: Database connection module utilizing psycopg2's `RealDictCursor`.
- `schema.sql`: PostgreSQL database schema with required tables and indexes.
- `.env`: Environment file containing sensitive credentials (e.g. `DATABASE_URL`).
- `requirements.txt`: Python package dependencies.
- `README.md`: Project setup and usage instructions.

---

## Local Setup Instructions 💻

### 1. Database Setup
1. Create a free account at [Neon](https://neon.tech).
2. Create a new project in the Singapore (`ap-southeast-1`) region.
3. Open the **Neon SQL Editor** (or connect via your favorite database client) and run the SQL commands in [schema.sql](file:///c:/Users/thimo/OneDrive/Documents/subscription-watchdog-m1/subscription-watchdog-m3/schema.sql) to create the tables, defaults, generated columns, and indexes.

### 2. Environment Configuration
Create a `.env` file in this directory and populate it with your connection string:
```env
DATABASE_URL=postgresql://user:password@ep-xyz.ap-southeast-1.aws.neon.tech/watchdog_db?sslmode=require
```

### 3. Installation
Activate the virtual environment and install the required dependencies:
```bash
# On Windows:
.venv\Scripts\activate

# Install dependencies:
pip install -r requirements.txt
```

---

## Running the Server 🏃‍♂️

Start the server using:
```bash
python server.py
```
This runs the FastMCP server with the **Streamable HTTP** transport listening on port `8000` (`http://0.0.0.0:8000`).

---

## Local Testing with MCP Inspector 🔍

You can inspect and test the MCP tools locally using the **Model Context Protocol Inspector**:
```bash
# Start inspector pointing to the server script
npx @modelcontextprotocol/inspector python server.py
```

This will run the server in `stdio` mode and launch a web interface at `http://localhost:5173` (or another port outputted in terminal) where you can interactively trigger the tools:
- **`add_sub`**: Test adding a subscription, verifying price updates (which inserts into `price_history`), and refreshes.
- **`get_subs`**: Retrieve subscriptions filtered by user, status, confidence, and category, and ensure `prev_price` is correctly populated.
- **`flag_sub`**: Flag an existing subscription for a specific reason (e.g., price spike).

---

## Deployment to Railway ☁️

To deploy this service and make it accessible to Member 2 (Extraction) and Member 4 (Decision Engine):

1. Initialize a Git repository in this subdirectory (or include it in your monorepo).
2. Connect the repository to [Railway](https://railway.app).
3. Set the `DATABASE_URL` environment variable in the Railway project dashboard.
4. Define the start command in Railway:
   ```bash
   python server.py
   ```
5. Share your public Railway service URL with M2 and M4:
   `https://your-app-name.up.railway.app/mcp`
