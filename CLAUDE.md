# Ghi chú cho Claude

- Trả lời người dùng bằng tiếng Việt.
- Đây là trang web tĩnh giới thiệu TTC Imperial Hotel Huế: ảnh tòa nhà → bấm tầng → mặt bằng cắt nóc → ảnh phòng. Không có bước build, không dùng thư viện ngoài. Chỉ có ba file mã: `index.html`, `style.css`, `main.js`.
- Phát hành: commit rồi đẩy thẳng lên `main` (GitHub Pages phục vụ từ `main`, thư mục gốc). Repo công khai — không đưa khóa, mật khẩu hay tài liệu nội bộ của khách sạn vào.

## Claude làm được gì, không làm được gì

- Claude **không tạo được ảnh chân thật hay video**. Mọi ảnh/video chân thật do người dùng tạo bằng Gemini (gói Pro của họ) rồi gửi lên; Claude viết câu lệnh, kiểm tra kết quả và ghép vào trang.
- Câu lệnh đã dùng nằm ở `ai-kit/HUONG-DAN.md` (ảnh) và `ai-kit/HUONG-DAN-VIDEO.md` (video). Khi cần cảnh mới, viết thêm mục vào đó theo đúng mẫu (Đính kèm / Lưu thành / câu lệnh tiếng Anh).
- Người dùng đã từ chối đưa khóa API Gemini và tài khoản Weave của họ là gói miễn phí (không chạy được mô hình video). Đừng hỏi lại hai thứ này trừ khi họ tự nhắc.
- Người dùng muốn hình **chân thật như ảnh chụp**; không gửi duyệt hình khối kiểu mô hình Blender.

## Dữ liệu và chỗ sửa

- Nội dung hạng phòng, điểm bấm, ảnh gắn với điểm bấm: `ROOMS` trong `main.js`. Tên hạng phòng, diện tích, số lượng phòng, mô tả là số liệu người dùng đưa — giữ nguyên văn.
- Tầng nào thuộc hạng phòng nào: `FLOOR_ROOM` trong `main.js`. Đây là **giả định**, chưa có sơ đồ thật.
- Vùng bấm từng tầng trên ảnh tòa nhà: `FLOOR_Y`, `floorPoly`, `LOBBY_POLY` trong `main.js`, đo theo `assets/hero/tower.jpg` (1792×2400). Đổi ảnh tòa nhà thì phải đo lại.
- Vị trí điểm bấm trên mặt bằng: `assets/turn/turn.json` (tính từ khung Blender, khung 00). Ảnh mặt bằng nào không cùng góc máy với khung đó thì khai `at` riêng trong `ROOMS` (xem `presidential`).
- Video chuyển cảnh: đặt file vào `assets/video/` đúng tên trong `VIDEOS` (`main.js`); trang tự phát, thiếu file thì dùng hiệu ứng phóng ảnh. Nén trước khi commit: `ffmpeg -i vào.mp4 -an -vf scale=1280:-2 -c:v libx264 -crf 26 -pix_fmt yuv420p -movflags +faststart ra.mp4`.
- Ảnh nhận từ Gemini có dấu sao ở góc dưới phải: xóa bằng bộ lọc `delogo` của ffmpeg hoặc để nằm trong vùng viền mờ. Đổi PNG sang JPG (`-q:v 3`) trước khi commit.

## Nhãn ảnh

- Ảnh thật của khách sạn ghi `'real'` (hiện "ảnh thật"); ảnh AI ghi `'ai'` (hiện "ảnh minh họa"). Không ghi ảnh AI là ảnh thật.

## Kiểm thử

- Chạy `python3 -m http.server 8000` rồi dùng Playwright mở trang ở cỡ 1280×800 và iPhone 13: bấm một tầng trên ảnh tòa nhà, bấm một điểm có ảnh, quay lại; không được có lỗi trang và không cuộn ngang.
- Chữ ≥ 11px; vùng bấm ≥ 32px trên máy tính, 44px trên điện thoại (biến `--hit` trong `style.css`).

## Việc còn dở

- Mặt bằng Grand Presidential do AI vẽ có ba giường (mô tả chỉ có một phòng ngủ chính) và ảnh chỉ rộng 1200 px — cần tạo lại.
- Junior Suite chưa có ảnh thật; ảnh phòng ngủ hiện là ảnh minh họa.
- Video Presidential bắt đầu từ một mặt bằng khác với ảnh `assets/plans/presidential.jpg` đang dùng — cần ảnh mặt bằng mới của người dùng để hai thứ khớp nhau.
- 3 căn hộ (Apartment) chưa đưa vào trang vì chưa có diện tích.
- Logo đang là chữ; chưa có file logo chính thức.
- `blender/` chỉ dùng để dựng lại khung bố cục khi cần góc máy mới (`pip install bpy`, rồi `python3 blender/render_rooms.py`); `tower.py` hiện không dùng trên web.
