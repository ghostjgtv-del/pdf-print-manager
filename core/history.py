"""
Print History Module - SQLite Database
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import csv


class HistoryManager:
    """Manages print history using SQLite"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default location
            app_data = Path.home() / '.pdf_print_manager'
            app_data.mkdir(parents=True, exist_ok=True)
            db_path = app_data / 'history.db'

        self.db_path = str(db_path)
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database and create tables if not exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS print_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    filepath TEXT NOT NULL,
                    printer TEXT NOT NULL,
                    pages INTEGER DEFAULT 0,
                    status TEXT NOT NULL,
                    error_message TEXT
                )
            ''')

            # Create index on timestamp for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON print_history(timestamp)
            ''')

            # Create index on status
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_status
                ON print_history(status)
            ''')

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error initializing database: {e}")

    def add_entry(self,
                  filename: str,
                  filepath: str,
                  printer: str,
                  pages: int = 0,
                  status: str = "Success",
                  error_message: str = None) -> bool:
        """
        Add a new history entry

        Args:
            filename: Name of the file
            filepath: Full path to the file
            printer: Printer name used
            pages: Number of pages (if known)
            status: Status (Success/Error)
            error_message: Error message if failed

        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            timestamp = datetime.now().isoformat()

            cursor.execute('''
                INSERT INTO print_history
                (timestamp, filename, filepath, printer, pages, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, filename, filepath, printer, pages, status, error_message))

            conn.commit()
            conn.close()

            return True

        except Exception as e:
            print(f"Error adding history entry: {e}")
            return False

    def get_history(self,
                    limit: int = 100,
                    status_filter: str = None,
                    date_from: datetime = None,
                    date_to: datetime = None) -> List[Dict]:
        """
        Get history entries with optional filters

        Args:
            limit: Maximum number of entries to return
            status_filter: Filter by status (Success/Error/None for all)
            date_from: Filter from this date
            date_to: Filter to this date

        Returns:
            List of history entries as dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Build query with filters
            query = "SELECT * FROM print_history WHERE 1=1"
            params = []

            if status_filter:
                query += " AND status = ?"
                params.append(status_filter)

            if date_from:
                query += " AND timestamp >= ?"
                params.append(date_from.isoformat())

            if date_to:
                query += " AND timestamp <= ?"
                params.append(date_to.isoformat())

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Convert to list of dicts
            entries = []
            for row in rows:
                entry = {
                    'id': row['id'],
                    'timestamp': datetime.fromisoformat(row['timestamp']),
                    'filename': row['filename'],
                    'filepath': row['filepath'],
                    'printer': row['printer'],
                    'pages': row['pages'],
                    'status': row['status'],
                    'error_message': row['error_message']
                }
                entries.append(entry)

            conn.close()
            return entries

        except Exception as e:
            print(f"Error retrieving history: {e}")
            return []

    def get_statistics(self) -> Dict:
        """
        Get statistics about print history

        Returns:
            Dictionary with statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            stats = {}

            # Total prints
            cursor.execute("SELECT COUNT(*) FROM print_history")
            stats['total_prints'] = cursor.fetchone()[0]

            # Successful prints
            cursor.execute("SELECT COUNT(*) FROM print_history WHERE status = 'Success'")
            stats['successful_prints'] = cursor.fetchone()[0]

            # Failed prints
            cursor.execute("SELECT COUNT(*) FROM print_history WHERE status = 'Error'")
            stats['failed_prints'] = cursor.fetchone()[0]

            # Total pages
            cursor.execute("SELECT SUM(pages) FROM print_history WHERE status = 'Success'")
            result = cursor.fetchone()[0]
            stats['total_pages'] = result if result else 0

            # Most used printer
            cursor.execute('''
                SELECT printer, COUNT(*) as count
                FROM print_history
                GROUP BY printer
                ORDER BY count DESC
                LIMIT 1
            ''')
            result = cursor.fetchone()
            stats['most_used_printer'] = result[0] if result else "N/A"

            # First print date
            cursor.execute("SELECT MIN(timestamp) FROM print_history")
            result = cursor.fetchone()[0]
            stats['first_print_date'] = datetime.fromisoformat(result) if result else None

            # Last print date
            cursor.execute("SELECT MAX(timestamp) FROM print_history")
            result = cursor.fetchone()[0]
            stats['last_print_date'] = datetime.fromisoformat(result) if result else None

            conn.close()
            return stats

        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}

    def export_to_csv(self, output_path: str, date_from: datetime = None, date_to: datetime = None) -> bool:
        """
        Export history to CSV file

        Args:
            output_path: Path for output CSV file
            date_from: Optional start date filter
            date_to: Optional end date filter

        Returns:
            True if successful
        """
        try:
            # Get all history entries
            entries = self.get_history(
                limit=999999,  # Get all
                date_from=date_from,
                date_to=date_to
            )

            if not entries:
                return False

            # Write to CSV
            with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['timestamp', 'filename', 'filepath', 'printer', 'pages', 'status', 'error_message']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for entry in entries:
                    # Format timestamp for CSV
                    entry_copy = entry.copy()
                    entry_copy['timestamp'] = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow(entry_copy)

            return True

        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    def clear_history(self, date_before: datetime = None) -> bool:
        """
        Clear history entries

        Args:
            date_before: Only clear entries before this date (None = clear all)

        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if date_before:
                cursor.execute(
                    "DELETE FROM print_history WHERE timestamp < ?",
                    (date_before.isoformat(),)
                )
            else:
                cursor.execute("DELETE FROM print_history")

            conn.commit()
            conn.close()

            return True

        except Exception as e:
            print(f"Error clearing history: {e}")
            return False

    def delete_entry(self, entry_id: int) -> bool:
        """Delete a specific entry by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM print_history WHERE id = ?", (entry_id,))

            conn.commit()
            conn.close()

            return True

        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False
