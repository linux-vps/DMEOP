# Ứng dụng hỗ trợ học tiếng Anh hiệu quả DM EOP

## Nội dung
- [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)
  - [Cài đặt Python](#cài-đặt-python)
  - [Cài đặt Tesseract](#cài-đặt-tesseract)
  - [Cài đặt FFmpeg](#cài-đặt-ffmpeg)
  - [Cài đặt ứng dụng DM EOP](#cài-đặt-ứng-dụng-dm-eop)

## Hướng dẫn cài đặt

### Cài đặt Python
Có nhiều cách để cài Python, có thể tải trong Microsoft Store hoặc xem hướng dẫn trên Youtube, hoặc theo hướng dẫn dưới đây:
1. Truy cập trang chính thức của Python: [python.org](https://www.python.org/downloads/)
2. Tải xuống phiên bản Python phù hợp với hệ điều hành của bạn.
3. Chạy trình cài đặt và đảm bảo chọn tùy chọn "Add Python to PATH" trước khi nhấn "Install Now".
4. Kiểm tra việc cài đặt bằng cách mở Command Prompt (Windows) hoặc Terminal (macOS/Linux) và chạy lệnh:

   ```bash
   python --version

Nếu báo lỗi, vui lòng copy lỗi lên google hoặc youtube xem hướng dẫn

### Cài đặt Tesseract

1. Truy cập trang chính thức của Tesseract: [tesseract-ocr.github.io](https://tesseract-ocr.github.io/)
2. Tải xuống trình cài đặt Tesseract cho Windows từ https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe
3. Chạy tệp cài đặt vừa tải xuống và làm theo hướng dẫn trên màn hình.
4. Khi cài đặt xong, đảm bảo rằng thư mục chứa `tesseract.exe` đã được thêm vào biến môi trường PATH. Thông thường, thư mục này là `C:\Program Files\Tesseract-OCR` hoặc tương tự.
   - Để thêm vào PATH, mở **Control Panel** > **System and Security** > **System** > **Advanced system settings** > **Environment Variables**. Trong phần **System variables**, tìm biến `Path`, chọn và nhấn **Edit**, sau đó thêm đường dẫn `C:\Program Files\Tesseract-OCR`.
5. Kiểm tra việc cài đặt bằng cách mở Command Prompt và chạy lệnh:

   ```bash
   tesseract --version
   ```
   
Nếu gặp vấn đề, hãy tìm kiếm lỗi trên Google hoặc YouTube để tìm giải pháp.
