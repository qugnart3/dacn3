import os

def create_directory_structure():
    # Lấy đường dẫn hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tạo cấu trúc thư mục
    directories = [
        os.path.join(current_dir, "DataSet", "train"),
        os.path.join(current_dir, "DataSet", "test"),
        os.path.join(current_dir, "DataSet", "all"),
        os.path.join(current_dir, "Dictionary"),
        os.path.join(current_dir, "HisFeedBack")
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Tạo các file cần thiết
    files = [
        os.path.join(current_dir, "DataSet", "train", "sents.txt"),
        os.path.join(current_dir, "DataSet", "train", "sentiments.txt"),
        os.path.join(current_dir, "DataSet", "test", "sents.txt"),
        os.path.join(current_dir, "DataSet", "test", "sentiments.txt"),
        os.path.join(current_dir, "DataSet", "all", "sents.txt"),
        os.path.join(current_dir, "Dictionary", "spell_correct_word.json"),
        os.path.join(current_dir, "HisFeedBack", "Positive.txt"),
        os.path.join(current_dir, "HisFeedBack", "Negative.txt")
    ]
    
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w', encoding='utf-8') as f:
                f.write('')
            print(f"Created file: {file}")

if __name__ == "__main__":
    create_directory_structure() 