def format_benchmark_stats(stats):
    """
    Hàm định dạng chuỗi hiển thị thông số Benchmark.
    Giữ nguyên 100% logic định dạng và comment tiếng Việt gốc.
    """
    if not stats:
        return "Đang đợi nước đi..."
        
    text = (
        f"Nước đi: Hàng {stats['move'][0]}, Cột {stats['move'][1]}\n"
        f"Điểm (Score): {stats['score']}\n"
        f"Độ sâu (Depth): {stats['depth']}\n"
        f"Trạng thái đã xét: {stats['states']}\n"
        f"Thời gian: {stats['time']:.4f} giây"
    )
    return text
