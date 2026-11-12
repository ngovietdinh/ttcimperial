# Bộ tạo video chuyển cảnh bằng Gemini (Veo)

Cách làm mỗi video: mở gemini.google.com → chọn "Tạo video" → đính kèm **một ảnh** ghi ở mục "Ảnh bắt đầu" → dán nguyên câu lệnh → tải video về (file .mp4, không quay màn hình).
Chọn khung hình ngang 16:9. Không cần tiếng.
Đặt tên file đúng như mục "Lưu thành" rồi gửi lại cho tôi: tôi nén lại, đưa vào `assets/video/`, trang web tự phát khi chuyển cảnh.

Làm video số 1 trước và gửi tôi xem. Video nào chưa có thì chỗ đó vẫn chuyển cảnh kiểu phóng ảnh như hiện nay.

Lưu ý chung: nếu video tự thêm người, chữ, hay đổi kiểu tòa nhà/đồ đạc, gõ tiếp bên dưới "same shot, but do not add people or text, keep the building/furniture unchanged".

---

## 1. Tòa nhà → bay vào tầng (dùng chung cho mọi tầng)
Ảnh bắt đầu: ảnh tòa nhà lúc chạng vạng (`assets/hero/tower.jpg`).
Lưu thành: `tower-in.mp4`

```
Start exactly from this image. Smooth cinematic drone shot: the camera slowly rises and flies forward toward the middle floors of the hotel tower, getting closer and closer to the warm lit windows and balconies until one glowing window fills the whole frame and the image blooms into soft warm golden light. Constant gentle speed, no cuts, no camera shake. Keep the building's architecture, roofs and lighting exactly as in the image. Blue hour, no people, no text. 6 seconds.
```

## 2. Tòa nhà → vào sảnh
Ảnh bắt đầu: ảnh tòa nhà lúc chạng vạng.
Lưu thành: `lobby-in.mp4`

```
Start exactly from this image. Smooth cinematic drone shot: the camera glides down and forward toward the lit entrance pavilion with the two-tier tiled roof at the bottom right, passes under the pavilion roof between its red columns and moves toward the glowing entrance doors until warm golden light fills the frame. Constant gentle speed, no cuts. Keep the building exactly as in the image. No people, no cars, no text. 6 seconds.
```

## 3. Deluxe: mặt bằng → phòng ngủ
Ảnh bắt đầu: mặt bằng cắt nóc Deluxe (`assets/plans/deluxe.jpg`).
Lưu thành: `deluxe-bedroom.mp4`

```
Start exactly from this image of a hotel room cutaway model. Smooth cinematic camera move: the camera descends from above and glides down into the bedroom area, ending at standing eye level at the foot of the bed, looking toward the bed with its carved dark wood headboard and the bright window with gold curtains. As the camera goes down, the room feels full size and real, with a ceiling coming into view. Keep all furniture, colours and materials exactly as in the image. Constant gentle speed, no cuts. No people, no text. 6 seconds.
```

## 4. Junior Suite: mặt bằng → phòng ngủ
Ảnh bắt đầu: mặt bằng cắt nóc Junior Suite (`assets/plans/junior.jpg`).
Lưu thành: `junior-bedroom.mp4`

```
Start exactly from this image of a hotel junior suite cutaway model. Smooth cinematic camera move: the camera descends from above and glides down into the room, ending at standing eye level near the entrance side, looking across the bed with the olive-green tufted headboard toward the sofa corner and the window with gold curtains. As the camera goes down, the room feels full size and real, with a ceiling coming into view. Keep all furniture, colours and materials exactly as in the image. Constant gentle speed, no cuts. No people, no text. 6 seconds.
```

## 5. Imperial Suite: mặt bằng → phòng khách
Ảnh bắt đầu: mặt bằng cắt nóc Imperial Suite (`assets/plans/imperial.jpg`).
Lưu thành: `imperial-living.mp4`

```
Start exactly from this image of a two-room hotel suite cutaway model. Smooth cinematic camera move: the camera descends from above and glides down into the living room, ending at standing eye level near the dining table, looking across the red and gold rug, the brown velvet sofa and orange armchairs toward the gold lattice partition with the round moon-gate opening and the bedroom behind it. As the camera goes down, the room feels full size and real, with a ceiling coming into view. Keep all furniture, colours and materials exactly as in the image. Constant gentle speed, no cuts. No people, no text. 6 seconds.
```

## 6. Imperial Suite: mặt bằng → góc ngồi bên cửa sổ
Ảnh bắt đầu: mặt bằng cắt nóc Imperial Suite.
Lưu thành: `imperial-window.mp4`

```
Start exactly from this image of a two-room hotel suite cutaway model. Smooth cinematic camera move: the camera descends from above and glides down into the living room, ending at seated eye level beside the brown velvet sofa, looking over the glass coffee table toward the two orange velvet armchairs and the tall windows with sheer white curtains and gold drapes glowing with daylight. Keep all furniture, colours and materials exactly as in the image. Constant gentle speed, no cuts. No people, no text. 6 seconds.
```

## 7. Grand Presidential: mặt bằng → phòng khách
Ảnh bắt đầu: mặt bằng cắt nóc Grand Presidential (`assets/plans/presidential.jpg`).
Lưu thành: `presidential-living.mp4`

```
Start exactly from this image of a large presidential suite cutaway model. Smooth cinematic camera move: the camera descends from above and glides down into the main living room, ending at seated eye level on the sofa side, looking past the glass coffee table and the orange velvet armchairs toward large corner windows with gold drapes and a warm sunset sky outside. Keep all furniture, colours and materials exactly as in the image. Constant gentle speed, no cuts. No people, no text. 6 seconds.
```
