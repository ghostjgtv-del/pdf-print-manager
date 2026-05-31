"""
PDF Printer Module
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group

Handles PDF printing using Windows print spooler
"""

import win32print
import win32api
import os
import subprocess
import winreg
import time
from pathlib import Path
from typing import List, Tuple
import threading


class PrintJob:
    """Represents a single print job"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.status = "Pending"  # Pending, Printing, Printed, Error
        self.error_message = ""
        self.page_count = self._get_page_count()

    def _get_page_count(self) -> int:
        """
        Try to get PDF page count
        Returns 0 if unable to determine
        """
        try:
            from PyPDF2 import PdfReader
            with open(self.filepath, 'rb') as f:
                pdf = PdfReader(f)
                num_pages = len(pdf.pages)
                return num_pages if num_pages > 0 else 0
        except ImportError:
            # PyPDF2 not available
            return 0
        except Exception as e:
            # Error reading PDF
            print(f"Error reading page count for {self.filename}: {e}")
            return 0

    def __repr__(self):
        return f"PrintJob({self.filename}, {self.status})"


def find_adobe_reader():
    """Busca Adobe Reader o Acrobat en las ubicaciones comunes de instalación."""
    possible_paths = [
        r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
        r"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
        r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
        r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
        r"C:\Program Files\Adobe\Reader 11.0\Reader\AcroRd32.exe",
        r"C:\Program Files (x86)\Adobe\Reader 11.0\Reader\AcroRd32.exe",
    ]

    # También buscar en el registro
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\AcroRd32.exe")
        adobe_path, _ = winreg.QueryValueEx(key, "")
        winreg.CloseKey(key)
        if os.path.exists(adobe_path):
            return adobe_path
    except:
        pass

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\AcroRd32.exe")
        adobe_path, _ = winreg.QueryValueEx(key, "")
        winreg.CloseKey(key)
        if os.path.exists(adobe_path):
            return adobe_path
    except:
        pass

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None


class PrinterManager:
    """Manages printer operations"""

    def __init__(self):
        self.printers = []
        self.default_printer = None
        self.refresh_printers()

    def refresh_printers(self) -> None:
        """Refresh list of available printers"""
        try:
            # Get all printers
            flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            printers = win32print.EnumPrinters(flags, None, 2)

            self.printers = [printer['pPrinterName'] for printer in printers]

            # Get default printer
            try:
                self.default_printer = win32print.GetDefaultPrinter()
            except Exception:
                # No default printer set
                self.default_printer = self.printers[0] if self.printers else None

        except Exception as e:
            print(f"Error enumerating printers: {e}")
            self.printers = []
            self.default_printer = None

    def get_printers(self) -> List[str]:
        """Get list of available printer names"""
        return self.printers

    def get_default_printer(self) -> str:
        """Get default printer name"""
        return self.default_printer

    def set_default_printer(self, printer_name: str) -> bool:
        """Set a printer as default"""
        try:
            win32print.SetDefaultPrinter(printer_name)
            self.default_printer = printer_name
            return True
        except Exception as e:
            print(f"Error setting default printer: {e}")
            return False

    def get_pdf_page_count(self, filepath: str) -> int:
        """
        Get the number of pages in a PDF file

        Args:
            filepath: Path to PDF file

        Returns:
            Number of pages (0 if unable to determine)
        """
        try:
            from PyPDF2 import PdfReader
            with open(filepath, 'rb') as f:
                pdf = PdfReader(f)
                num_pages = len(pdf.pages)
                return num_pages if num_pages > 0 else 0
        except ImportError:
            # PyPDF2 not available
            return 0
        except Exception as e:
            # Error reading PDF
            print(f"Error reading page count for {filepath}: {e}")
            return 0

    def print_pdf(self, filepath: str, printer_name: str = None) -> Tuple[bool, str]:
        """
        Genera archivo temporal PDF y lo envía a la impresora especificada.
        Intenta usar Adobe Reader si está instalado, o usa win32print directamente.

        Args:
            filepath: Path to PDF file
            printer_name: Target printer (None for default)

        Returns:
            Tuple of (success, message)
        """
        try:
            # Validate file exists
            if not os.path.exists(filepath):
                return False, f"File not found: {filepath}"

            # Use default printer if none specified
            if not printer_name:
                printer_name = self.default_printer

            if not printer_name:
                return False, "No printer available"

            success = False

            # ==========================================
            # Método 1: Adobe Reader (más confiable)
            # ==========================================
            adobe_path = find_adobe_reader()
            if adobe_path and printer_name:
                try:
                    # /t = print to printer and terminate
                    subprocess.run(
                        [adobe_path, "/t", filepath, printer_name],
                        timeout=30,
                        creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                    )
                    success = True
                    time.sleep(2)  # Dar tiempo para que Adobe envíe el trabajo al spooler
                    return True, "✓ Sent to printer via Adobe Reader"
                except Exception as e:
                    print(f"Adobe print failed: {e}")
                    success = False

            # ==========================================
            # Método 2: win32print directo (respaldo)
            # ==========================================
            if not success and printer_name:
                try:
                    # Establecer la impresora como predeterminada temporalmente
                    original_printer = None
                    try:
                        original_printer = win32print.GetDefaultPrinter()
                        if original_printer != printer_name:
                            win32print.SetDefaultPrinter(printer_name)
                            time.sleep(0.3)
                    except:
                        pass

                    # Abrir el PDF y enviarlo al spooler usando win32print
                    hprinter = win32print.OpenPrinter(printer_name)
                    try:
                        # Leer el contenido del PDF
                        with open(filepath, "rb") as f:
                            pdf_data = f.read()

                        # Crear un trabajo de impresión
                        job_info = (os.path.basename(filepath), None, "RAW")
                        job_id = win32print.StartDocPrinter(hprinter, 1, job_info)
                        win32print.StartPagePrinter(hprinter)
                        win32print.WritePrinter(hprinter, pdf_data)
                        win32print.EndPagePrinter(hprinter)
                        win32print.EndDocPrinter(hprinter)
                        success = True
                    finally:
                        win32print.ClosePrinter(hprinter)

                    # Restaurar impresora original
                    if original_printer and original_printer != printer_name:
                        try:
                            win32print.SetDefaultPrinter(original_printer)
                        except:
                            pass

                    if success:
                        return True, "✓ Sent to printer"

                except Exception as e:
                    print(f"Win32print failed: {e}")
                    # Último intento: usar método tradicional
                    try:
                        # Restaurar impresora si hubo error
                        if original_printer and original_printer != printer_name:
                            try:
                                win32print.SetDefaultPrinter(original_printer)
                            except:
                                pass

                        # Intentar ShellExecute
                        if printer_name != self.default_printer:
                            try:
                                win32print.SetDefaultPrinter(printer_name)
                                time.sleep(0.3)
                            except:
                                pass

                        result = win32api.ShellExecute(0, "print", filepath, None, ".", 0)

                        if printer_name != self.default_printer and original_printer:
                            try:
                                win32print.SetDefaultPrinter(original_printer)
                            except:
                                pass

                        if result > 32:
                            return True, "✓ Sent to printer"

                    except Exception:
                        pass

            # Si todo falló
            if not success:
                return False, (
                    "Unable to print. Please try one of these solutions:\n\n"
                    "1. Install Adobe Acrobat Reader DC (recommended)\n"
                    "   Download: https://get.adobe.com/reader/\n\n"
                    "2. Verify your printer supports direct PDF printing\n\n"
                    "3. Set a PDF viewer as default:\n"
                    "   Settings → Apps → Default apps → PDF"
                )

        except Exception as e:
            return False, f"Print error: {str(e)}"

    def print_multiple(self,
                      jobs: List[PrintJob],
                      printer_name: str = None,
                      wait_seconds: int = 3,
                      progress_callback=None) -> Tuple[int, int, List[str]]:
        """
        Print multiple PDF files

        Args:
            jobs: List of PrintJob objects
            printer_name: Target printer (None for default)
            wait_seconds: Seconds to wait between prints
            progress_callback: Function(current, total, job) called after each file

        Returns:
            Tuple of (successful_count, failed_count, error_list)
        """
        import time

        successful = 0
        failed = 0
        errors = []

        for i, job in enumerate(jobs):
            if job.status != "Pending":
                continue

            # Update status
            job.status = "Printing"

            if progress_callback:
                progress_callback(i + 1, len(jobs), job)

            # Print the file
            success, message = self.print_pdf(job.filepath, printer_name)

            if success:
                job.status = "Printed"
                successful += 1
            else:
                job.status = "Error"
                job.error_message = message
                failed += 1
                errors.append(f"{job.filename}: {message}")

            # Wait between prints (except for last one)
            if i < len(jobs) - 1:
                time.sleep(wait_seconds)

        return successful, failed, errors

    def print_multiple_async(self,
                            jobs: List[PrintJob],
                            printer_name: str = None,
                            wait_seconds: int = 3,
                            progress_callback=None,
                            completion_callback=None) -> threading.Thread:
        """
        Print multiple PDFs in a background thread

        Args:
            jobs: List of PrintJob objects
            printer_name: Target printer
            wait_seconds: Seconds between prints
            progress_callback: Function(current, total, job)
            completion_callback: Function(successful, failed, errors)

        Returns:
            The thread object
        """
        def worker():
            result = self.print_multiple(
                jobs,
                printer_name,
                wait_seconds,
                progress_callback
            )

            if completion_callback:
                completion_callback(*result)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread


class PrintQueue:
    """Manages a queue of print jobs"""

    def __init__(self):
        self.jobs: List[PrintJob] = []

    def add_file(self, filepath: str) -> PrintJob:
        """Add a single file to queue"""
        job = PrintJob(filepath)
        self.jobs.append(job)
        return job

    def add_files(self, filepaths: List[str]) -> List[PrintJob]:
        """Add multiple files to queue"""
        added_jobs = []
        for filepath in filepaths:
            job = self.add_file(filepath)
            added_jobs.append(job)
        return added_jobs

    def add_folder(self, folder_path: str, recursive: bool = False) -> List[PrintJob]:
        """Add all PDFs from a folder"""
        added_jobs = []
        folder = Path(folder_path)

        if not folder.exists() or not folder.is_dir():
            return added_jobs

        # Get PDF files
        if recursive:
            pdf_files = folder.rglob("*.pdf")
        else:
            pdf_files = folder.glob("*.pdf")

        for pdf_file in sorted(pdf_files):
            job = self.add_file(str(pdf_file))
            added_jobs.append(job)

        return added_jobs

    def remove_job(self, index: int) -> bool:
        """Remove a job by index"""
        try:
            if 0 <= index < len(self.jobs):
                self.jobs.pop(index)
                return True
            return False
        except Exception:
            return False

    def clear(self) -> None:
        """Clear all jobs"""
        self.jobs.clear()

    def clear_printed(self) -> None:
        """Remove all printed/error jobs"""
        self.jobs = [job for job in self.jobs if job.status == "Pending"]

    def move_up(self, index: int) -> bool:
        """Move job up in queue"""
        if 0 < index < len(self.jobs):
            self.jobs[index], self.jobs[index - 1] = self.jobs[index - 1], self.jobs[index]
            return True
        return False

    def move_down(self, index: int) -> bool:
        """Move job down in queue"""
        if 0 <= index < len(self.jobs) - 1:
            self.jobs[index], self.jobs[index + 1] = self.jobs[index + 1], self.jobs[index]
            return True
        return False

    def get_pending_jobs(self) -> List[PrintJob]:
        """Get only pending jobs"""
        return [job for job in self.jobs if job.status == "Pending"]

    def get_job_count(self) -> int:
        """Get total job count"""
        return len(self.jobs)

    def get_pending_count(self) -> int:
        """Get pending job count"""
        return len(self.get_pending_jobs())

    def get_total_pages(self) -> int:
        """Get total page count (for jobs with known page count)"""
        return sum(job.page_count for job in self.jobs if job.page_count > 0)
