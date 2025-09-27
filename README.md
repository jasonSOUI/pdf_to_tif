# PDF 轉 TIF 轉換器

一個簡單的 Python 應用程式，用於將 PDF 檔案轉換為黑白的 TIF 圖片，並提供桌面 GUI 和網頁兩種操作介面。

## 功能特性

- **雙介面**: 提供傳統的桌面應用程式 (GUI) 和現代化的網頁瀏覽器介面 (Web UI)。
- **可攜性**: 專案內建 Poppler 依賴，在大多數情況下無需額外下載或設定即可運作。
- **易於使用**: 透過簡單的批次檔 (`.bat`) 即可啟動。
- **彈性設定**: 支援 LZW 和 CCITT T.6 兩種 TIF 壓縮演算法。

---

## 如何使用

### 步驟 1: 安裝依賴 (僅需執行一次)

在開始前，您需要安裝本專案所需的 Python 套件。

1.  在專案資料夾中，開啟命令提示字元 (CMD)。
2.  執行以下指令：
    ```sh
    pip install -r requirements.txt
    ```

### 步驟 2: 選擇一種方式啟動應用程式

您可以在桌面版或網頁版之間任選其一。

#### 選項 A: 網頁版 (建議)

1.  雙擊 `start_web_server.bat` 檔案。
2.  命令提示字元會顯示伺服器已啟動。
3.  打開您的網頁瀏覽器 (如 Chrome, Edge, Firefox)，在網址列輸入： `http://127.0.0.1:28888`
4.  透過網頁介面進行操作。

#### 選項 B: 桌面版

1.  雙擊 `start_converter.bat` 檔案。
2.  程式的圖形化介面將會直接開啟。

---

## 進階設定 (可選)

### 自訂 Poppler 路徑

本專案已包含 Poppler 工具，應可直接運作。但如果您想使用系統中已安裝或特定版本的 Poppler，可以透過以下方式自訂路徑：

1.  在專案根目錄手動建立一個 `config.ini` 檔案。
2.  在檔案中輸入以下內容，並將路徑替換為您 Poppler 的 `bin` 資料夾實際路徑：

**`config.ini` 範例：**
```ini
[Settings]
poppler_path = C:\path\to\your\poppler-version\Library\bin
```
程式在啟動時會優先使用此設定檔中的路徑。

## 應用程式截圖 (GUI 版本)

![example.png](https://github.com/jasonSOUI/pdf_to_tif/blob/main/example.png)
