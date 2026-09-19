"""
Main Application Entry Point - 2EZ4U Food Delivery
Mata Kuliah: Struktur Data & Analisa Algoritma (EC234303) - FTEIC ITS

Jalankan dengan perintah:
    python app.py
"""

import tkinter as tk
from frontend.ui import AppUI


def main():
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
