import pandas as pd
import os

def save_all_excel_sheets_as_csv(excel_file_path, output_dir="data"):
    """
    Membaca semua sheet dari file Excel dan menyimpannya sebagai file CSV terpisah.

    Args:
        excel_file_path (str): Path lengkap ke file Excel (.xlsx).
        output_dir (str): Direktori tempat file CSV akan disimpan. Akan dibuat jika tidak ada.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Direktori '{output_dir}' berhasil dibuat.")

    try:
        # Membaca semua sheet dari file Excel
        xls = pd.ExcelFile(excel_file_path)
        sheet_names = xls.sheet_names
        print(f"Ditemukan {len(sheet_names)} sheet: {sheet_names}")

        for sheet_name in sheet_names:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            
            # Sanitasi nama sheet untuk nama file CSV (misal: ganti spasi dengan underscore)
            sanitized_sheet_name = sheet_name.replace(" ", "_").replace("&", "and").replace(",", "") # Tambahkan sanitasi lain jika perlu
            csv_file_name = f"{sanitized_sheet_name}.csv"
            csv_file_path = os.path.join(output_dir, csv_file_name)
            
            df.to_csv(csv_file_path, index=False, encoding='utf-8')
            print(f"Sheet '{sheet_name}' berhasil disimpan sebagai '{csv_file_name}'")

    except FileNotFoundError:
        print(f"Error: File Excel tidak ditemukan di '{excel_file_path}'")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# --- Cara Penggunaan ---
if __name__ == "__main__":
    # Pastikan path ini benar sesuai lokasi file Excel Anda
    # Asumsikan file Excel berada di direktori yang sama dengan script ini,
    # atau sesuaikan path-nya.
    excel_file = "retail_analysis_results.xlsx"

    # Direktori output (akan dibuat di root proyek Django Anda)
    output_directory = "data" # Ini akan membuat folder 'data' di mana script ini dijalankan

    # save_all_excel_sheets_as_csv(excel_file, output_directory)
    # print("\nProses selesai. Cek folder 'data' Anda.")

    # Jika Anda juga ingin menyimpan sheet dari 'Online Retail.xlsx'
    # Pastikan file tersebut sudah ada di lokasi yang sama atau sesuaikan path
    online_retail_excel_file = "Online Retail.xlsx"
    save_all_excel_sheets_as_csv(online_retail_excel_file, output_directory)
    # print("\nProses untuk Online Retail.xlsx selesai.")