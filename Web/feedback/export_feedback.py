import os
import sys
import django
from datetime import datetime

# Thêm đường dẫn của project vào PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Web.settings')
django.setup()

# Import sau khi đã setup Django
from feedback.models import Feedback

def export_feedback():
    # Tạo thư mục exports nếu chưa có
    output_dir = os.path.join(current_dir, 'exports')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tạo tên file với timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    positive_file = os.path.join(output_dir, f'positive_{timestamp}.txt')
    neutral_file = os.path.join(output_dir, f'neutral_{timestamp}.txt')
    negative_file = os.path.join(output_dir, f'negative_{timestamp}.txt')

    # Lấy feedback theo từng loại sentiment
    positive_feedback = Feedback.objects.filter(sentiment='Positive')
    neutral_feedback = Feedback.objects.filter(sentiment='Neutral')
    negative_feedback = Feedback.objects.filter(sentiment='Negative')

    # Ghi vào file positive
    with open(positive_file, 'w', encoding='utf-8') as f:
        f.write(f"=== Feedback tích cực ({positive_feedback.count()} items) ===\n\n")
        for fb in positive_feedback:
            f.write(f"Text: {fb.text}\n")
            f.write(f"Độ tin cậy: {fb.confidence*100:.2f}%\n")
            f.write("-" * 50 + "\n")

    # Ghi vào file neutral
    with open(neutral_file, 'w', encoding='utf-8') as f:
        f.write(f"=== Feedback trung lập ({neutral_feedback.count()} items) ===\n\n")
        for fb in neutral_feedback:
            f.write(f"Text: {fb.text}\n")
            f.write(f"Độ tin cậy: {fb.confidence*100:.2f}%\n")
            f.write("-" * 50 + "\n")

    # Ghi vào file negative
    with open(negative_file, 'w', encoding='utf-8') as f:
        f.write(f"=== Feedback tiêu cực ({negative_feedback.count()} items) ===\n\n")
        for fb in negative_feedback:
            f.write(f"Text: {fb.text}\n")
            f.write(f"Độ tin cậy: {fb.confidence*100:.2f}%\n")
            f.write("-" * 50 + "\n")

    print(f'Đã xuất feedback ra các file:')
    print(f'- Tích cực: {positive_file}')
    print(f'- Trung lập: {neutral_file}')
    print(f'- Tiêu cực: {negative_file}')

if __name__ == '__main__':
    export_feedback() 