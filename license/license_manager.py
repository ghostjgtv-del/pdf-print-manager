"""
License Manager for PDF Print Manager
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
Date: May 2026
"""

import os
import json
import hashlib
import hmac
from datetime import datetime, timedelta
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import requests
import platform
import uuid


class LicenseManager:
    """Manages license validation and storage"""

    # Secret key for HMAC (this should be kept secret in production)
    # In a real deployment, consider using environment variables or obfuscation
    _SECRET_KEY = b'LFFG_PDF_PRINT_MANAGER_2026_JT_SECRET_KEY_V1'

    # Server configuration
    SERVER_URL = "http://143.110.130.78:8001"

    def __init__(self):
        self.license_file = Path.home() / '.pdf_print_manager' / '.license.dat'
        self.license_file.parent.mkdir(parents=True, exist_ok=True)
        self._cipher = self._get_cipher()
        self.pc_id = self._get_pc_id()

    def _get_pc_id(self) -> str:
        """Generate unique PC identifier"""
        try:
            # Use MAC address + hostname for unique ID
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                          for elements in range(0,2*6,2)][::-1])
            hostname = platform.node()
            pc_id = f"PC-{hashlib.md5(f'{mac}{hostname}'.encode()).hexdigest()[:8].upper()}"
            return pc_id
        except:
            return f"PC-{uuid.uuid4().hex[:8].upper()}"

    def _get_cipher(self) -> Fernet:
        """Generate Fernet cipher from secret key"""
        key = base64.urlsafe_b64encode(hashlib.sha256(self._SECRET_KEY).digest())
        return Fernet(key)

    def _generate_signature(self, client_id: str, issue_date: str, duration_days: int) -> str:
        """Generate HMAC signature for license validation"""
        data = f"{client_id}:{issue_date}:{duration_days}".encode()
        signature = hmac.new(self._SECRET_KEY, data, hashlib.sha256).hexdigest()[:8]
        return signature.upper()

    def _encode_component(self, value: str, length: int = 4) -> str:
        """Encode a string into alphanumeric format"""
        hash_obj = hashlib.md5(value.encode())
        encoded = base64.b32encode(hash_obj.digest()).decode()[:length]
        return encoded.upper()

    def _decode_date(self, encoded: str) -> datetime:
        """Decode date from hex format"""
        try:
            # Decode from hex (8 characters = 4 bytes)
            timestamp = int(encoded, 16)
            return datetime.fromtimestamp(timestamp)
        except:
            # Fallback for invalid encoding
            return datetime.now()

    def _encode_date(self, date: datetime) -> str:
        """Encode date to hex format (8 characters)"""
        timestamp = int(date.timestamp())
        # Convert to hex, remove '0x' prefix, pad to 8 chars, uppercase
        return format(timestamp, '08X')

    def _decode_duration(self, encoded: str) -> int:
        """Decode duration from hex format"""
        try:
            # Decode from hex (4 characters = 2 bytes)
            return int(encoded, 16)
        except:
            return 0

    def _encode_duration(self, days: int) -> str:
        """Encode duration to hex format (4 characters)"""
        # Convert to hex, remove '0x' prefix, pad to 4 chars, uppercase
        return format(days, '04X')

    def generate_license_code(self, client_id: str, duration_days: int) -> tuple[str, datetime]:
        """
        Generate a license code

        Args:
            client_id: Unique identifier for the client (e.g., "LFFG-PROD")
            duration_days: Number of days the license is valid

        Returns:
            tuple: (license_code, expiration_date)
        """
        issue_date = datetime.now()
        expiration_date = issue_date + timedelta(days=duration_days)

        # Format: LFFG-XXXX-XXXXXXXX-XXXX-XXXXXXXX
        prefix = "LFFG"
        client_hash = self._encode_component(client_id, 4)
        date_encoded = self._encode_date(issue_date)  # 8 chars (hex)
        duration_encoded = self._encode_duration(duration_days)  # 4 chars (hex)
        signature = self._generate_signature(client_id, issue_date.isoformat(), duration_days)

        license_code = f"{prefix}-{client_hash}-{date_encoded}-{duration_encoded}-{signature}"

        return license_code, expiration_date

    def validate_license_code(self, license_code: str) -> tuple[bool, str, datetime | None]:
        """
        Validate a license code against the server

        Args:
            license_code: The license code to validate

        Returns:
            tuple: (is_valid, message, expiration_date)
        """
        try:
            # Validate against server
            response = requests.post(
                f"{self.SERVER_URL}/license/validate",
                json={
                    "license_code": license_code.strip(),
                    "pc_id": self.pc_id
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()

                if result.get("valid"):
                    license_info = result.get("license_info", {})
                    days_remaining = license_info.get("days_remaining", 0)
                    expiration_date_str = license_info.get("expiration_date", "")

                    # Parse expiration date
                    try:
                        expiration_date = datetime.fromisoformat(expiration_date_str)
                    except:
                        expiration_date = datetime.now() + timedelta(days=days_remaining)

                    return True, f"Licencia válida. {days_remaining} días restantes", expiration_date
                else:
                    message = result.get("message", "Licencia inválida")
                    return False, message, None
            else:
                return False, "Error al validar con el servidor", None

        except requests.exceptions.ConnectionError:
            return False, "No se puede conectar al servidor de licencias", None
        except requests.exceptions.Timeout:
            return False, "Tiempo de espera agotado al conectar con el servidor", None
        except Exception as e:
            return False, f"Error al validar licencia: {str(e)}", None

    def save_license(self, license_code: str) -> tuple[bool, str]:
        """
        Save validated license to encrypted file

        Args:
            license_code: The license code to save

        Returns:
            tuple: (success, message)
        """
        # Validate before saving
        is_valid, message, expiration_date = self.validate_license_code(license_code)

        if not is_valid:
            return False, message

        try:
            # Create license data
            license_data = {
                'code': license_code,
                'activated_at': datetime.now().isoformat(),
                'expires_at': expiration_date.isoformat()
            }

            # Encrypt and save
            json_data = json.dumps(license_data).encode()
            encrypted_data = self._cipher.encrypt(json_data)

            with open(self.license_file, 'wb') as f:
                f.write(encrypted_data)

            return True, message

        except Exception as e:
            return False, f"Error al guardar licencia: {str(e)}"

    def load_license(self) -> tuple[bool, str, int]:
        """
        Load and validate stored license

        Returns:
            tuple: (is_valid, message, days_remaining)
        """
        if not self.license_file.exists():
            return False, "No se encontró licencia. Por favor, active la aplicación.", 0

        try:
            # Read and decrypt
            with open(self.license_file, 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = self._cipher.decrypt(encrypted_data)
            license_data = json.loads(decrypted_data.decode())

            # Validate expiration
            expiration_date = datetime.fromisoformat(license_data['expires_at'])

            if datetime.now() > expiration_date:
                return False, f"Licencia expirada el {expiration_date.strftime('%Y-%m-%d')}", 0

            days_remaining = (expiration_date - datetime.now()).days

            # Warning if less than 7 days
            if days_remaining <= 7:
                return True, f"⚠️ Licencia expira pronto: {days_remaining} días restantes", days_remaining

            return True, f"Licencia válida. {days_remaining} días restantes", days_remaining

        except Exception as e:
            return False, f"Error al cargar licencia: {str(e)}", 0

    def get_license_info(self) -> dict | None:
        """Get detailed license information"""
        if not self.license_file.exists():
            return None

        try:
            with open(self.license_file, 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = self._cipher.decrypt(encrypted_data)
            license_data = json.loads(decrypted_data.decode())

            expiration_date = datetime.fromisoformat(license_data['expires_at'])
            activated_date = datetime.fromisoformat(license_data['activated_at'])
            days_remaining = (expiration_date - datetime.now()).days

            return {
                'code': license_data['code'],
                'activated_at': activated_date,
                'expires_at': expiration_date,
                'days_remaining': days_remaining,
                'is_valid': datetime.now() <= expiration_date
            }

        except Exception:
            return None

    def delete_license(self) -> bool:
        """Delete stored license"""
        try:
            if self.license_file.exists():
                self.license_file.unlink()
            return True
        except Exception:
            return False
