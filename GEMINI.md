# 專案目標

一個可攜式的 Python 桌面應用程式，提供圖形化介面 (GUI)，用於將 PDF 檔案轉換為黑白的 TIF 檔案。

# 技術棧與架構

*   **語言**: Python
*   **GUI 框架**: `Tkinter` (標準函式庫)
*   **核心依賴**: 
    *   `pdf2image`: Python 的 Poppler 外包裝 (Wrapper)。
    *   `Pillow`: 用於圖像處理與儲存。
    *   `Poppler`: 實際的 PDF 轉換引擎，**以子目錄的形式被捆綁在專案中**，而非外部安裝。

# 關鍵設計規劃

1.  **可攜性 (Portability)**:
    *   專案的核心設計目標是可攜性。`main.py` 中的 `POPPLER_PATH` **不是寫死的絕對路徑**。
    *   程式在啟動時，會使用 `os.path.dirname(os.path.abspath(__file__))` 來動態偵測自身位置，並以此為基準，建立指向捆綁的 `poppler-25.07.0/Library/bin` 資料夾的相對路徑。
    *   這使得整個專案資料夾可以被放置在使用者電腦的任何位置，都能正常運作。

2.  **UI 回應性 (Responsiveness)**:
    *   轉換過程 (`_perform_conversion` 函式) 是在一個獨立的 `threading.Thread` 中執行的。
    *   這個設計可以防止在處理大型或多個 PDF 檔案時，主 GUI 視窗發生凍結或無回應的情況，提升了使用者體驗。

3.  **依賴管理 (Dependency Management)**:
    *   **Python 套件**: 所有需要的 Python 函式庫都記錄在 `requirements.txt` 中，可透過 `pip install -r requirements.txt` 一鍵安裝。
    *   **二進位檔依賴**: `Poppler` 工具集作為一個子資料夾直接包含在專案中，使用者無需額外下載或設定環境變數，大大簡化了部署的複雜度。

4.  **使用者體驗 (UX)**:
    *   **啟動器**: 提供 `start_converter.bat` 批次檔，使用 `pyw.exe` 執行，實現無主控台視窗的乾淨啟動體驗。
    *   **預設路徑**: 預設的儲存位置會自動設定為使用者的「下載」資料夾，提升便利性。
    *   **即時回饋**: GUI 介面會顯示轉換的即時狀態與進度。

# 主要檔案結構

*   `main.py`: 包含 `PDFConverterApp` 類別的應用程式主體。
*   `requirements.txt`: Python 相依套件列表。
*   `start_converter.bat`: Windows 快速啟動器。
*   `README.md`: 給使用者的操作手冊。
*   `poppler-25.07.0/`: 捆綁的 Poppler 執行環境。
*   `GEMINI.md`: (本檔案) 專案的技術架構備忘，供 Gemini 參考。