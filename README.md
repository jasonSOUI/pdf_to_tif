# PDF 轉 TIF 轉換器

一個簡單的桌面應用程式，用於將 PDF 檔案轉換為黑白的 TIF 圖片。

## ⚠️ 重要：首次使用前必須手動設定

本專案不包含 Poppler 引擎，您必須手動下載並設定路徑才能執行。

### 設定步驟

1.  **下載 Poppler**: 請從[此推薦來源](https://github.com/oschwartz10612/poppler-windows/releases/)下載最新的二進位檔案。
2.  **解壓縮 Poppler**: 將下載的 `.zip` 檔案解壓縮到您電腦的任意位置 (例如：`C:\poppler-24.02.0`)。
3.  **設定路徑**:
    *   打開專案中的 `config.ini` 檔案。
    *   找到 `[Settings]` 下的 `poppler_path` 項目。
    *   在等號後面填入您剛剛解壓縮的 Poppler `bin` 資料夾的**完整路徑**。

**`config.ini` 範例：**
```ini
[Settings]
poppler_path = C:\poppler-24.02.0\Library\bin
```
4.  **安裝 Python 依賴**:
    *   在專案目錄開啟命令提示字元，執行 `pip install -r requirements.txt`。

## 如何執行

完成上述設定後，雙擊 `start_converter.bat` 來執行應用程式。

## 功能特性

-   選擇一個或多個 PDF 檔案。
-   選擇儲存轉換後 TIF 檔案的目錄。
-   即時進度顯示。