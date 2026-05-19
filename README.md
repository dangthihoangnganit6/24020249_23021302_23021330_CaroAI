# Dự án Game Caro AI 9x9 - Minimax & Alpha-Beta Pruning

Dự án này là chương trình trò chơi cờ Caro kích thước 9x9, hỗ trợ người chơi đấu với máy tính thông qua các thuật toán tìm kiếm đối kháng kinh điển. Dự án được phát triển như một bài tập lớn cho môn Trí tuệ nhân tạo (UET).

## 1. Giới thiệu chung
- Kích thước bàn cờ: 9x9 (BOARD_SIZE = 9).
- Luật thắng: Đạt chuỗi 4 quân liên tiếp (ngang, dọc, chéo). Không áp dụng luật chặn hai đầu.
- Công nghệ sử dụng: Ngôn ngữ Python 3.x, giao diện đồ họa Tkinter.
- Thuật toán AI:
  - Minimax: Duyệt toàn bộ cây quyết định theo độ sâu cấu hình.
  - Alpha-Beta Pruning: Cắt tỉa các nhánh vô hiệu để tối ưu thời gian phản hồi.
  - Heuristic Evaluation: Hàm đánh giá trạng thái bàn cờ dựa trên bộ trọng số ưu tiên phòng ngự.

## 2. Cấu trúc thư mục dự án
- source_code/ (Thư mục chứa toàn bộ mã nguồn của chương trình)
  - main.py: Điểm khởi chạy chương trình (Giao diện đồ họa GUI)
  - logic.py: Hàm xử lý luật chơi, kiểm tra thắng/thua và đánh giá Heuristic
  - minimax.py: Cài đặt thuật toán Minimax
  - alphabeta.py: Cài đặt thuật toán Alpha-Beta Pruning
  - constants.py: Chứa các hằng số cấu hình hệ thống (Kích thước, Điểm số, Độ sâu)
  - benchmark.py: Định dạng và cấu trúc hiển thị các thông số hiệu năng
  - run_experiments.py: Kịch bản thực nghiệm tự động trên 6 trạng thái bàn cờ mẫu
- requirements.txt: Khai báo môi trường và cấu hình cài đặt
- README.md: File hướng dẫn và mô tả chi tiết hệ thống

## 3. Hướng dẫn cài đặt và khởi chạy

### Yêu cầu hệ thống
- Máy tính đã cài đặt Python 3.8 trở lên.
- Thư viện giao diện Tkinter (Thường đi kèm sẵn khi cài đặt Python trên Windows/macOS. Đối với Linux/Ubuntu, vui lòng chạy lệnh "sudo apt-get install python3-tk" để cài đặt nhân đồ họa).

### Cách chạy chương trình chính (Giao diện đồ họa)
1. Mở Terminal hoặc Command Prompt, di chuyển vào thư mục source_code.
2. Khởi chạy chương trình bằng câu lệnh:
   python main.py
3. At menu chính, bạn có thể thiết lập:
   - Chọn độ sâu tìm kiếm chiến thuật (Depth 1-3).
   - Chọn chế độ vận hành đối kháng với thuật toán Minimax hoặc Alpha-Beta.
   - Kích hoạt "Chế độ Thực nghiệm" để quan sát AI xử lý trực tiếp các thế cờ biểu mẫu có sẵn.

### Cách chạy kịch bản thực nghiệm tự động (Terminal)
Để so sánh định lượng trực diện hiệu suất giữa Minimax và Alpha-Beta (về tổng số trạng thái đã xét và thời gian chạy thực tế):
1. Di chuyển vào thư mục source_code.
2. Khởi chạy tiến trình kiểm thử tự động bằng câu lệnh:
   python run_experiments.py

## 4. Hướng dẫn tương tác ván đấu
- Người chơi (X): Nhấp chuột trái vào ô trống bất kỳ trên ma trận bàn cờ để hạ quân.
- Máy tính (O): Tự động phân tích, tính toán chiến thuật và phản hồi ngay sau lượt đi của con người.
- Bảng thông số cấu hình: Phía bên phải màn hình hiển thị báo cáo thời gian thực bao gồm:
  - Tọa độ nước đi tác tử AI vừa lựa chọn.
  - Điểm số Heuristic tĩnh tại trạng thái hiện tại.
  - Tổng số trạng thái (Nodes) mà hệ thống đã thực duyệt trên cây quyết định.
  - Thời gian xử lý logic tính bằng giây.

## 5. Tính năng tối ưu nâng cao
- Chiến lược Move Ordering: Tại phương thức get_refined_moves, các nước đi ứng viên được sắp xếp phân cấp nghiêm ngặt qua Tuple (-best_chain, -nearby_count, dist_to_center). Cơ chế này ép cây quyết định tiếp cận nhánh tối ưu sớm nhất, giúp tăng tốc hiệu quả cắt tỉa của Alpha-Beta lên hơn 90%.
- Cơ chế Neighbor Radius: Thu hẹp vùng biên tìm kiếm trong phạm vi lân cận NEIGHBOR_RADIUS = 2 tính từ các ô đã có quân, ngăn chặn hoàn toàn hiện tượng bùng nổ tổ hợp trạng thái thừa trên bàn cờ.
- Hệ thống Real-time Benchmark: Cập nhật trực tiếp hiệu năng tài nguyên máy tính giúp định lượng sức mạnh thuật toán trực quan ngay trong phiên chạy.

## 6. Thông tin nhóm thực hiện
- Đơn vị công tác: Trường Đại học Công nghệ, Đại học Quốc gia Hà Nội (UET - VNU).
- Danh sách thành viên:
  - Đặng Thị Hoàng Ngân (MSV: 24020249)
  - Phạm Trường Long (MSV: 23021302)
  - Nguyễn Ngọc Như Quang (MSV: 23021328)
- Repository: https://github.com/dangthihoangnganit6/24020249_23021302_23021328_CaroAI.git