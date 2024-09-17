# Ứng dụng hỗ trợ học tiếng Anh hiệu quả DM EOP
- Source công khai, tuy khá đầy đủ nhưng anh em cần cải tiến nó ( tham gia [ĐM EOP](https://www.facebook.com/groups/1493850704586284).)
- Không phụ thuộc vào cấu trúc câu hỏi, miễn còn ra đáp án là còn dùng được.

## Nội dung
- [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)
  - [Cài đặt Tesseract](#cài-đặt-tesseract)
  - [Cài đặt FFmpeg](#cài-đặt-ffmpeg)
  - [Cài đặt ứng dụng DM EOP](#cài-đặt-ứng-dụng-dm-eop)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
- Hoặc tham gia vào nhóm cộng đồng để xem video hướng dẫn ở phần ghim: [ĐM EOP](https://www.facebook.com/groups/1493850704586284).
## Hướng dẫn cài đặt


### Cài đặt Tesseract

1. Tải xuống trình cài đặt Tesseract cho Windows từ https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe
2. Chạy tệp cài đặt vừa tải xuống và làm theo hướng dẫn trên màn hình.
3. Khi cài đặt xong, đảm bảo rằng thư mục chứa `tesseract.exe` đã được thêm vào biến môi trường PATH. Thông thường, thư mục này là `C:\Program Files\Tesseract-OCR` hoặc tương tự.
   - Để thêm vào PATH, mở **Control Panel** > **System and Security** > **System** > **Advanced system settings** > **Environment Variables**. Trong phần **System variables**, tìm biến `Path`, chọn và nhấn **Edit**, sau đó thêm đường dẫn `C:\Program Files\Tesseract-OCR`.
4. Kiểm tra việc cài đặt bằng cách mở Command Prompt và chạy lệnh:

   ```bash
   tesseract --version
   ```
5. Tải file dữ liệu dùng cho font chữ ( đã trained riêng cho eop ): [eng.zip](https://github.com/user-attachments/files/17023612/eng.zip)
6. Giải nén `eng.zip`, copy file `eng.traineddata` vào thư mục `C:\Program Files\Tesseract-OCR\tessdata`

Nếu gặp vấn đề, hãy tìm kiếm lỗi trên Google hoặc YouTube để tìm giải pháp.


### Cài đặt FFmpeg

1. Truy cập trang chính thức của FFmpeg: [ffmpeg.org](https://ffmpeg.org/download.html).
2. Tải xuống bản build FFmpeg cho Windows từ [đây](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z) hoặc [đây](https://www.btbn.net/ffmpeg-builds/).
3. Giải nén tệp tải về vào một thư mục, chẳng hạn như `C:\ffmpeg`.
4. Thêm thư mục chứa `ffmpeg.exe` vào biến môi trường PATH:
   - Mở **Control Panel** > **System and Security** > **System** > **Advanced system settings** > **Environment Variables**.
   - Trong phần **System variables**, tìm biến `Path`, chọn và nhấn **Edit**, sau đó thêm đường dẫn đến thư mục chứa `ffmpeg.exe` (ví dụ: `C:\ffmpeg\bin`).
5. Kiểm tra việc cài đặt bằng cách mở Command Prompt và chạy lệnh:

   ```bash
   ffmpeg -version
   ```

Nếu gặp vấn đề, hãy tìm kiếm lỗi trên Google hoặc YouTube để tìm giải pháp.
  
### Cài đặt ứng dụng DM EOP

1. Tải xuống thư mục và giải nén
3. Di chuyển ứng dụng ra ngoài desktop hoặc nơi muốn đặt và sử dụng

   
## Hướng dẫn sử dụng
- Nhập thời gian chờ ngẫu nhiên (Mặc định là 30 giây đến 60 giây)
- Nhập thông tin và ấn nút Start tương ứng
- Lưu ý: Lần chạy đầu tiên sẽ mất chút thời gian.
- Tham gia vào cộng đồng để giao lưu và trao đổi: https://t.me/dmeop
