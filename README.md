# TTC Imperial Hotel Huế — khám phá 3D

Trang web tĩnh: tòa nhà 3D → chọn tầng → mặt bằng 3D cắt nóc của hạng phòng → ảnh thật.

## Chạy thử

```
python3 -m http.server 8000     # rồi mở http://localhost:8000
```

Không cần bước build. Đưa nguyên thư mục lên bất kỳ dịch vụ web tĩnh nào (Vercel, Cloudflare Pages…).

## Cấu trúc

- `index.html`, `style.css`, `main.js` — trang web, không dùng thư viện ngoài.
- `assets/hero/tower.jpg` — ảnh tòa nhà (tạo bằng Gemini từ ảnh mặt tiền thật). Vùng bấm từng tầng khai báo trong `main.js` (`FLOOR_Y`).
- `assets/plans/*.jpg` — mặt bằng cắt nóc chân thật của bốn hạng phòng (tạo bằng Gemini từ khung bố cục Blender + ảnh thật).
- `assets/photos/` — ảnh phòng: ảnh thật của khách sạn, riêng `junior-bedroom.jpg` là ảnh minh họa AI.
- `assets/turn/turn.json` — vị trí điểm bấm trên mặt bằng, tính từ khung Blender.
- `blender/` — mã dựng khung bố cục: `rooms.py` + `render_rooms.py` (mặt bằng), `tower.py` (khối tòa nhà 3D, hiện không dùng trên web).
- `assets/video/` — video chuyển cảnh (tùy chọn). Tên file khai báo trong `main.js` (`VIDEOS`); có file nào trang phát file đó, thiếu thì chuyển cảnh bằng phóng ảnh.
- `ai-kit/` — ảnh bố cục và câu lệnh tạo ảnh (`HUONG-DAN.md`) và tạo video (`HUONG-DAN-VIDEO.md`) bằng Gemini.

## Chỗ đang là giả định (cần số liệu thật)

- Phân bổ tầng trong `main.js` (`FLOOR_ROOM`): tầng 5–12 Deluxe, 13–14 Junior Suite, 15 Imperial Suite, 16 Grand Presidential Suite.
- Bố trí bên trong từng phòng: phỏng dựng theo diện tích công bố, chưa theo bản vẽ.
- Ảnh tòa nhà và mặt bằng là ảnh minh họa AI, giống phong cách chứ không đúng từng chi tiết của công trình thật.
- Mặt bằng Grand Presidential do AI vẽ có ba giường, khác mô tả (một phòng ngủ chính).
- Ảnh nào thuộc hạng phòng nào (`ROOMS[...].spots` trong `main.js`).
