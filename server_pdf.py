"""
PDF Print Manager - FastAPI Server
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group

Server endpoints for:
- License management
- Print job tracking
- Auto-update system
- Activity logging
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
import sqlite3
import json
import os
import hashlib
import hmac
from pathlib import Path
from contextlib import contextmanager
import platform

app = FastAPI()

# ============================================================================
# Configuration
# ============================================================================

APP_NAME = "impresion_pdf"
HOST = "0.0.0.0"
PORT = 8001  # Puerto específico para PDF Print Manager

# Secret key for license HMAC (should match client)
_LICENSE_SECRET_KEY = b'LFFG_PDF_PRINT_MANAGER_2026_JT_SECRET_KEY_V1'

# Database path - Auto-detect OS
if platform.system() == "Windows":
    DB_PATH = r"C:\JG_Server\impresion_pdf_data.db"
    UPDATES_PATH = r"C:\JG_Server\impresion_pdf\updates"
    INSTALLER_PATH = r"C:\JG_Server\impresion_pdf\installer"
else:
    DB_PATH = "/opt/lagudi/impresion_pdf/impresion_pdf_data.db"
    UPDATES_PATH = "/opt/lagudi/impresion_pdf/updates"
    INSTALLER_PATH = "/opt/lagudi/impresion_pdf/installer"

# Create directories if they don't exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(UPDATES_PATH, exist_ok=True)
os.makedirs(INSTALLER_PATH, exist_ok=True)

# Auto-Update Configuration
APP_VERSION = "1.0"  # Current version available for download
APP_EXE_PATH = os.path.join(UPDATES_PATH, "impresion_pdf.exe")
INSTALLER_FILE = os.path.join(INSTALLER_PATH, f"ImpresionPDF_Setup_v{APP_VERSION}.exe")

# ============================================================================
# Request Models
# ============================================================================

class LogRequest(BaseModel):
    username: str
    action: str
    pc: str
    details: str = ""

class LicenseValidateRequest(BaseModel):
    license_code: str
    pc_id: str

class LicenseGenerateRequest(BaseModel):
    client_id: str
    duration_days: int
    notes: str = ""

class PrintJobRequest(BaseModel):
    username: str
    pc: str
    printer_name: str
    file_name: str
    pages: int
    status: str  # success, error, cancelled

# ============================================================================
# Database Connection Manager
# ============================================================================

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# ============================================================================
# Database Initialization
# ============================================================================

def init_database():
    """Initialize database and create tables if they don't exist"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Activity log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP NOT NULL,
                usuario TEXT NOT NULL,
                accion TEXT NOT NULL,
                pc TEXT NOT NULL,
                details TEXT
            )
        """)

        # Licenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_code TEXT UNIQUE NOT NULL,
                client_id TEXT NOT NULL,
                issue_date TIMESTAMP NOT NULL,
                expiration_date TIMESTAMP NOT NULL,
                duration_days INTEGER NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # License activations table (track which PCs have activated licenses)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS license_activations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_code TEXT NOT NULL,
                pc_id TEXT NOT NULL,
                pc_name TEXT,
                activated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_check TIMESTAMP,
                FOREIGN KEY (license_code) REFERENCES licenses(license_code)
            )
        """)

        # Print jobs history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS print_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP NOT NULL,
                usuario TEXT NOT NULL,
                pc TEXT NOT NULL,
                printer_name TEXT NOT NULL,
                file_name TEXT NOT NULL,
                pages INTEGER,
                status TEXT NOT NULL,
                error_message TEXT
            )
        """)

        conn.commit()

# Initialize database on startup
init_database()

# ============================================================================
# License Management Functions
# ============================================================================

def generate_license_signature(client_id: str, issue_date: str, duration_days: int) -> str:
    """Generate HMAC signature for license validation"""
    data = f"{client_id}:{issue_date}:{duration_days}".encode()
    signature = hmac.new(_LICENSE_SECRET_KEY, data, hashlib.sha256).hexdigest()[:8]
    return signature.upper()

def encode_date(date: datetime) -> str:
    """Encode date to hex format (8 characters)"""
    timestamp = int(date.timestamp())
    return format(timestamp, '08X')

def decode_date(encoded: str) -> datetime:
    """Decode date from hex format"""
    try:
        timestamp = int(encoded, 16)
        return datetime.fromtimestamp(timestamp)
    except:
        return datetime.now()

def encode_duration(days: int) -> str:
    """Encode duration to hex format (4 characters)"""
    return format(days, '04X')

def decode_duration(encoded: str) -> int:
    """Decode duration from hex format"""
    try:
        return int(encoded, 16)
    except:
        return 0

def encode_component(value: str, length: int = 4) -> str:
    """Encode a string into alphanumeric format"""
    hash_obj = hashlib.md5(value.encode())
    import base64
    encoded = base64.b32encode(hash_obj.digest()).decode()[:length]
    return encoded.upper()

# ============================================================================
# API Endpoints - Health Check
# ============================================================================

@app.get("/ping")
async def ping():
    """Health check endpoint"""
    try:
        return {
            "ok": True,
            "app": APP_NAME,
            "version": APP_VERSION,
            "message": "PDF Print Manager Server running"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ============================================================================
# API Endpoints - Activity Logging
# ============================================================================

@app.post("/log")
async def log_activity(request: LogRequest):
    """Log user activity"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO activity (fecha, usuario, accion, pc, details)
                VALUES (?, ?, ?, ?, ?)
            """, (datetime.now(), request.username, request.action, request.pc, request.details))

        return {"ok": True}

    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/activity")
async def get_activity():
    """Get activity log"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT fecha, usuario, accion, pc, details
                FROM activity
                ORDER BY fecha DESC
                LIMIT 1000
            """)

            activity_list = []
            for row in cursor.fetchall():
                activity_list.append({
                    "fecha": str(row['fecha']),
                    "usuario": row['usuario'],
                    "accion": row['accion'],
                    "pc": row['pc'],
                    "details": row['details'] or ""
                })

            return {"ok": True, "activity": activity_list}

    except Exception as e:
        return {"ok": False, "error": str(e)}

# ============================================================================
# API Endpoints - License Management
# ============================================================================

@app.post("/license/generate")
async def generate_license(request: LicenseGenerateRequest):
    """Generate a new license code"""
    try:
        issue_date = datetime.now()
        expiration_date = issue_date + timedelta(days=request.duration_days)

        # Generate license code: LFFG-XXXX-XXXXXXXX-XXXX-XXXXXXXX
        prefix = "LFFG"
        client_hash = encode_component(request.client_id, 4)
        date_encoded = encode_date(issue_date)
        duration_encoded = encode_duration(request.duration_days)
        signature = generate_license_signature(request.client_id, issue_date.isoformat(), request.duration_days)

        license_code = f"{prefix}-{client_hash}-{date_encoded}-{duration_encoded}-{signature}"

        # Store in database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO licenses (license_code, client_id, issue_date, expiration_date, duration_days, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (license_code, request.client_id, issue_date, expiration_date, request.duration_days, request.notes))

        return {
            "ok": True,
            "license_code": license_code,
            "client_id": request.client_id,
            "issue_date": issue_date.isoformat(),
            "expiration_date": expiration_date.isoformat(),
            "duration_days": request.duration_days
        }

    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.post("/license/validate")
async def validate_license(request: LicenseValidateRequest):
    """Validate a license code and track activation"""
    try:
        # Parse license code
        parts = request.license_code.strip().upper().split('-')

        if len(parts) != 5:
            return {"ok": False, "error": "Invalid license format"}

        prefix, client_hash, date_encoded, duration_encoded, signature = parts

        if prefix != "LFFG":
            return {"ok": False, "error": "Invalid license code"}

        # Decode date and duration
        try:
            issue_date = decode_date(date_encoded)
            duration_days = decode_duration(duration_encoded)
        except Exception:
            return {"ok": False, "error": "Corrupted license code"}

        # Calculate expiration
        expiration_date = issue_date + timedelta(days=duration_days)

        # Check if expired
        if datetime.now() > expiration_date:
            return {
                "ok": False,
                "error": f"License expired on {expiration_date.strftime('%Y-%m-%d')}",
                "expired": True
            }

        # Check if license exists in database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT client_id, expiration_date FROM licenses
                WHERE license_code = ?
            """, (request.license_code,))

            result = cursor.fetchone()

            if not result:
                # License not in database, but code is valid - add it
                cursor.execute("""
                    INSERT INTO licenses (license_code, client_id, issue_date, expiration_date, duration_days)
                    VALUES (?, ?, ?, ?, ?)
                """, (request.license_code, "UNKNOWN", issue_date, expiration_date, duration_days))

            # Track/update activation
            cursor.execute("""
                INSERT INTO license_activations (license_code, pc_id, last_check)
                VALUES (?, ?, ?)
                ON CONFLICT(license_code, pc_id) DO UPDATE SET last_check = ?
            """, (request.license_code, request.pc_id, datetime.now(), datetime.now()))

        days_remaining = (expiration_date - datetime.now()).days

        return {
            "ok": True,
            "valid": True,
            "expiration_date": expiration_date.isoformat(),
            "days_remaining": days_remaining,
            "message": f"License valid. {days_remaining} days remaining"
        }

    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/licenses")
async def get_licenses():
    """Get all licenses"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT license_code, client_id, issue_date, expiration_date, duration_days, notes, created_at
                FROM licenses
                ORDER BY created_at DESC
            """)

            licenses_list = []
            for row in cursor.fetchall():
                exp_date = datetime.fromisoformat(row['expiration_date'])
                days_remaining = (exp_date - datetime.now()).days
                is_expired = days_remaining < 0

                licenses_list.append({
                    "license_code": row['license_code'],
                    "client_id": row['client_id'],
                    "issue_date": str(row['issue_date']),
                    "expiration_date": str(row['expiration_date']),
                    "duration_days": row['duration_days'],
                    "days_remaining": days_remaining,
                    "expired": is_expired,
                    "notes": row['notes'] or "",
                    "created_at": str(row['created_at'])
                })

            return {"ok": True, "licenses": licenses_list}

    except Exception as e:
        return {"ok": False, "error": str(e)}

# ============================================================================
# API Endpoints - Print Job Tracking
# ============================================================================

@app.post("/print/log")
async def log_print_job(request: PrintJobRequest):
    """Log a print job"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO print_jobs (fecha, usuario, pc, printer_name, file_name, pages, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (datetime.now(), request.username, request.pc, request.printer_name,
                  request.file_name, request.pages, request.status, request.details if hasattr(request, 'details') else None))

        return {"ok": True}

    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/print/history")
async def get_print_history():
    """Get print job history"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT fecha, usuario, pc, printer_name, file_name, pages, status, error_message
                FROM print_jobs
                ORDER BY fecha DESC
                LIMIT 500
            """)

            jobs_list = []
            for row in cursor.fetchall():
                jobs_list.append({
                    "fecha": str(row['fecha']),
                    "usuario": row['usuario'],
                    "pc": row['pc'],
                    "printer_name": row['printer_name'],
                    "file_name": row['file_name'],
                    "pages": row['pages'],
                    "status": row['status'],
                    "error_message": row['error_message'] or ""
                })

            return {"ok": True, "jobs": jobs_list}

    except Exception as e:
        return {"ok": False, "error": str(e)}

# ============================================================================
# API Endpoints - Auto-Update System
# ============================================================================

@app.get("/app/version")
async def get_app_version():
    """Return current version available for download"""
    try:
        return {
            "ok": True,
            "version": APP_VERSION,
            "file_exists": os.path.exists(APP_EXE_PATH)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/app/download")
async def download_app():
    """Serve the application .exe file for download"""
    try:
        if not os.path.exists(APP_EXE_PATH):
            raise HTTPException(status_code=404, detail="Application file not found")

        return FileResponse(
            path=APP_EXE_PATH,
            media_type="application/octet-stream",
            filename="impresion_pdf.exe"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/installer")
async def download_installer():
    """Download the PDF Print Manager installer"""
    try:
        if not os.path.exists(INSTALLER_FILE):
            raise HTTPException(status_code=404, detail="Installer not found")

        return FileResponse(
            path=INSTALLER_FILE,
            media_type="application/octet-stream",
            filename=f"ImpresionPDF_Setup_v{APP_VERSION}.exe"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Server Startup
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("  JG SERVER - PDF Print Manager Backend")
    print("  Lagudis Fresh Food Group")
    print("=" * 70)
    print(f"  App Name: {APP_NAME}")
    print(f"  Listening on: http://{HOST}:{PORT}")
    print(f"  Database: {DB_PATH}")
    print(f"  App Version: {APP_VERSION}")
    print(f"  Updates Path: {UPDATES_PATH}")
    print("=" * 70)
    uvicorn.run(app, host=HOST, port=PORT)
