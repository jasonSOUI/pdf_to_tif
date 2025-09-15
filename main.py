import os
import sys
import threading
import configparser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image

# --- 常數設定 ---

# 基準路徑偵測
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Poppler 路徑設定 ---
# 預設路徑 (後備方案)
default_poppler_path = os.path.join(script_dir, "poppler-25.07.0", "Library", "bin")
POPPLER_PATH = default_poppler_path # 先給定預設值

# 優先從 config.ini 讀取
config = configparser.ConfigParser()
config_file = os.path.join(script_dir, 'config.ini')

if os.path.exists(config_file):
    try:
        config.read(config_file, encoding='utf-8')
        if 'Settings' in config and 'poppler_path' in config['Settings']:
            config_path = config['Settings']['poppler_path'].strip()
            if config_path: # 如果路徑不是空白
                POPPLER_PATH = config_path
    except Exception as e:
        # 如果設定檔讀取錯誤，可以選擇忽略或提示，這裡選擇忽略，繼續使用預設路徑
        print(f"讀取 config.ini 時發生錯誤: {e}")

class PDFConverterApp:
    """一個將 PDF 轉換為 TIF 的 Tkinter GUI 應用程式"""

    def __init__(self, root):
        """初始化應用程式"""
        self.root = root
        self.root.title("PDF 轉 TIF 轉換器")
        self.root.geometry("700x550")
        self.root.minsize(600, 450)

        self.pdf_files = []
        
        # --- 設定預設儲存路徑 ---
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.isdir(downloads_folder):
            downloads_folder = os.path.expanduser("~") # 如果找不到 Downloads，則退回到使用者主目錄
        self.output_folder = tk.StringVar(value=downloads_folder)


        # --- UI 樣式設定 ---
        style = ttk.Style()
        style.configure("TButton", padding=6, font=('Helvetica', 10))
        style.configure("TLabel", font=('Helvetica', 10))
        style.configure("TFrame", padding=10)
        style.configure("Header.TLabel", font=('Helvetica', 14, 'bold'))

        # --- 主框架 ---
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- 檔案選擇區 ---
        files_frame = ttk.LabelFrame(main_frame, text="1. 選擇 PDF 檔案", padding=(10, 5))
        files_frame.pack(fill=tk.X, pady=5)

        self.select_files_button = ttk.Button(files_frame, text="選擇檔案...", command=self.select_pdf_files)
        self.select_files_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_list_button = ttk.Button(files_frame, text="清除列表", command=self.clear_file_list)
        self.clear_list_button.pack(side=tk.LEFT)

        # --- 檔案列表 ---
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(expand=True, fill=tk.BOTH, pady=5)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # --- 輸出路徑區 ---
        output_frame = ttk.LabelFrame(main_frame, text="2. 選擇儲存位置", padding=(10, 5))
        output_frame.pack(fill=tk.X, pady=5)

        # 縮短顯示路徑以適應 UI
        display_path = self.output_folder.get()
        if len(display_path) > 50:
            display_path = "..." + display_path[-47:]
        self.output_label = ttk.Label(output_frame, text=display_path, background="#eee", padding=5)
        self.output_label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        self.select_output_button = ttk.Button(output_frame, text="瀏覽...", command=self.select_output_folder)
        self.select_output_button.pack(side=tk.LEFT)

        # --- 執行與狀態區 ---
        action_frame = ttk.LabelFrame(main_frame, text="3. 執行與狀態", padding=(10, 5))
        action_frame.pack(fill=tk.X, pady=5)

        # --- 壓縮選項 ---
        compression_frame = ttk.Frame(action_frame)
        compression_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(compression_frame, text="壓縮格式:").pack(side=tk.LEFT, padx=(0, 5))

        self.compression_method = tk.StringVar(value="LZW")
        self.compression_combo = ttk.Combobox(
            compression_frame, 
            textvariable=self.compression_method, 
            values=["CCITT T.6", "LZW"], 
            state="readonly",
            width=12
        )
        self.compression_combo.pack(side=tk.LEFT)

        self.convert_button = ttk.Button(action_frame, text="開始轉換", command=self.start_conversion_thread)
        self.convert_button.pack(pady=5)

        self.status_label = ttk.Label(action_frame, text="請先選擇檔案和儲存位置")
        self.status_label.pack(pady=5)

    def select_pdf_files(self):
        """開啟對話框以選擇多個 PDF 檔案"""
        files = filedialog.askopenfilenames(
            title="請選擇 PDF 檔案",
            filetypes=[("PDF 檔案", "*.pdf"), ("所有檔案", "*.* ")]
        )
        if files:
            for f in files:
                if f not in self.file_listbox.get(0, tk.END):
                    self.file_listbox.insert(tk.END, f)
            self.update_status(f"{len(self.file_listbox.get(0, tk.END))} 個檔案已加入列表。")

    def clear_file_list(self):
        """清除檔案列表"""
        self.file_listbox.delete(0, tk.END)
        self.update_status("檔案列表已清除。")

    def select_output_folder(self):
        """開啟對話框以選擇儲存資料夾"""
        folder = filedialog.askdirectory(title="請選擇儲存 TIF 檔案的資料夾")
        if folder:
            self.output_folder.set(folder)
            # 縮短顯示路徑以適應 UI
            display_path = folder
            if len(display_path) > 50:
                display_path = "..." + display_path[-47:]
            self.output_label.config(text=display_path)
            self.update_status("儲存位置已設定。")

    def update_status(self, message):
        """更新狀態標籤的文字"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def start_conversion_thread(self):
        """在新的執行緒中啟動轉換過程，以避免 GUI 凍結"""
        self.pdf_files = self.file_listbox.get(0, tk.END)
        output_dir = self.output_folder.get()

        if not self.pdf_files:
            messagebox.showerror("錯誤", "請至少選擇一個 PDF 檔案！")
            return
        if not output_dir:
            messagebox.showerror("錯誤", "請選擇一個儲存位置！")
            return

        # 禁用按鈕，防止重複點擊
        self.convert_button.config(state=tk.DISABLED)
        self.select_files_button.config(state=tk.DISABLED)
        self.select_output_button.config(state=tk.DISABLED)
        self.clear_list_button.config(state=tk.DISABLED)
        self.compression_combo.config(state=tk.DISABLED) # 禁用下拉選單

        # 獲取選擇的壓縮方法
        compression_choice = self.compression_method.get()

        # 啟動執行緒
        thread = threading.Thread(target=self._perform_conversion, args=(self.pdf_files, output_dir, compression_choice))
        thread.daemon = True
        thread.start()

    def _perform_conversion(self, pdf_files, output_dir, compression_choice):
        """核心轉換邏輯"""
        # 映射 UI 選項到 Pillow 的參數
        compression_map = {
            "CCITT T.6": "group4",
            "LZW": "tiff_lzw"
        }
        compression_algorithm = compression_map.get(compression_choice, "group4") # 預設為 group4

        total_files = len(pdf_files)
        for i, pdf_path in enumerate(pdf_files):
            filename = os.path.basename(pdf_path)
            self.update_status(f"({i+1}/{total_files}) 正在轉換: {filename}...")

            try:
                # Convert PDF to a list of PIL images
                # POPPLER_PATH is defined globally at the top of the script
                images = convert_from_path(
                    pdf_path,
                    dpi=300,
                    poppler_path=POPPLER_PATH,
                    grayscale=True
                )

                # 將圖片物件轉為 1-bit 黑白模式
                bw_images = [img.convert('1') for img in images]

                # 設定 TIF 檔名並儲存
                tif_filename = os.path.splitext(filename)[0] + '.tif'
                tif_path = os.path.join(output_dir, tif_filename)

                bw_images[0].save(
                    tif_path,
                    'TIFF',
                    save_all=True,
                    append_images=bw_images[1:],
                    compression=compression_algorithm,
                    dpi=(204, 196)
                )

            except Exception as e:
                error_message = f"轉換 {filename} 時發生錯誤: {e}"
                self.update_status(error_message)
                messagebox.showerror("轉換錯誤", error_message)
                # 發生錯誤時，跳出迴圈
                break
        else: # for 迴圈正常結束時執行
            self.update_status(f"全部 {total_files} 個檔案轉換完成！")
            messagebox.showinfo("成功", "所有選定的 PDF 檔案都已成功轉換！")

        # 無論成功或失敗，都重新啟用按鈕
        self.convert_button.config(state=tk.NORMAL)
        self.select_files_button.config(state=tk.NORMAL)
        self.select_output_button.config(state=tk.NORMAL)
        self.clear_list_button.config(state=tk.NORMAL)
        self.compression_combo.config(state=tk.NORMAL) # 啟用下拉選單


if __name__ == '__main__':
    # 檢查 Poppler 路徑是否存在
    if not os.path.isdir(POPPLER_PATH):
        messagebox.showerror(
            "Poppler 未找到",
            f"錯誤：找不到 Poppler 工具路徑！\n請確認 Poppler 已解壓縮，且路徑設定正確。\n\n目前設定的路徑是：\n{POPPLER_PATH}"
        )
    else:
        root = tk.Tk()
        app = PDFConverterApp(root)
        root.mainloop()