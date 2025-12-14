import os

# Konfigurasi: Folder/File yang ingin DIABAIKAN (agar tidak terlalu berat)
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', 'env', '.idea', '.vscode', 'dist', 'build'}
IGNORE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.exe', '.pyc', '.zip', '.mp3', '.mp4'}

def merge_files(output_file='full_codebase.txt'):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Tulis struktur folder di awal
        outfile.write("=== STRUKTUR FILE ===\n")
        for root, dirs, files in os.walk('.'):
            # Filter folder yang diabaikan
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            level = root.replace('.', '').count(os.sep)
            indent = ' ' * 4 * (level)
            outfile.write('{}{}/\n'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if not any(f.endswith(ext) for ext in IGNORE_EXTS):
                    outfile.write('{}{}\n'.format(subindent, f))
        
        outfile.write("\n\n=== ISI FILE ===\n\n")

        # Tulis isi setiap file
        for root, dirs, files in os.walk('.'):k
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file == 'gabung_code.py' or file == output_file:
                    continue # Jangan masukkan script ini sendiri
                
                # Skip file binary/gambar
                if any(file.endswith(ext) for ext in IGNORE_EXTS):
                    continue

                path = os.path.join(root, file)
                
                try:
                    with open(path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(f"\n{'='*20}\nFILE: {path}\n{'='*20}\n")
                        outfile.write(content + "\n")
                except Exception as e:
                    print(f"Gagal membaca {path}: {e}")

    print(f"Selesai! Semua kode ada di file: {output_file}")

if __name__ == "__main__":
    merge_files()