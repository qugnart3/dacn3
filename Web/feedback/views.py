from django.shortcuts import render
from django.http import JsonResponse
from .models import Feedback
import sys
import os
import traceback

# Lấy đường dẫn tuyệt đối
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, '..', 'Model', 'Source')
MODEL_PATH = os.path.join(MODEL_DIR, 'SetModel', 'NotProcess', 'Model')

print("Checking paths:")
print(f"BASE_DIR: {BASE_DIR}")
print(f"MODEL_DIR: {MODEL_DIR}")
print(f"MODEL_PATH: {MODEL_PATH}")

# Thêm đường dẫn đến thư mục chứa model
sys.path.append(MODEL_DIR)

# Khởi tạo biến global
model = None
acronym = None

def initialize_model():
    global model, acronym
    try:
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        print(f"Model directory exists: {os.path.exists(MODEL_DIR)}")
        print(f"Model path exists: {os.path.exists(MODEL_PATH)}")
        
        # Import các module cần thiết
        from SetModel import Model
        from VniAcronym import Acronym
        
        # Khởi tạo model
        print("Initializing model...")
        model = Model(MODEL_PATH)
        print("Model initialized successfully!")

        # Thay đổi working directory tạm thời để load file Acronym.json
        original_dir = os.getcwd()
        os.chdir(MODEL_DIR)
        try:
            print("Initializing acronym...")
            acronym = Acronym()
            print("Acronym initialized successfully!")
        finally:
            os.chdir(original_dir)

    except Exception as e:
        import traceback
        print(f"Error during initialization: {str(e)}")
        print("Full traceback:")
        print(traceback.format_exc())
        model = None
        acronym = None

# Khởi tạo model khi module được load
initialize_model()

def home(request):
    try:
        # Thử khởi tạo lại model nếu chưa được khởi tạo
        if not model or not acronym:
            initialize_model()
        
        # Kiểm tra trạng thái model và acronym
        model_status = "Model is initialized" if model else "Model failed to initialize"
        acronym_status = "Acronym is initialized" if acronym else "Acronym failed to initialize"
        print(f"Status - {model_status}, {acronym_status}")

        if not model or not acronym:
            return render(request, 'feedback/home.html', {
                'error': f'Initialization error. {model_status}. {acronym_status}.',
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0
            })

        # Lấy thống kê
        positive_count = Feedback.objects.filter(sentiment='Positive').count()
        negative_count = Feedback.objects.filter(sentiment='Negative').count()
        neutral_count = Feedback.objects.filter(sentiment='Neutral').count()
        
        context = {
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total_count': positive_count + negative_count + neutral_count
        }
        return render(request, 'feedback/home.html', context)
    except Exception as e:
        print(f"Error in home view: {str(e)}")
        return render(request, 'feedback/home.html', {'error': str(e)})

def analyze_feedback(request):
    if request.method == 'POST':
        try:
            # Thử khởi tạo lại model nếu chưa được khởi tạo
            if not model or not acronym:
                initialize_model()

            text = request.POST.get('text', '')
            if not text:
                return JsonResponse({'error': 'Text is required'}, status=400)
            
            if not model:
                return JsonResponse({'error': 'Model not initialized'}, status=500)
            if not acronym:
                return JsonResponse({'error': 'Acronym processor not initialized'}, status=500)

            # Xử lý từ viết tắt
            processed_text = acronym.Solve_Acr(text)
            # Dự đoán sentiment
            label, confidence = model.Predict(processed_text)
            
            # Lưu vào database
            feedback = Feedback.objects.create(
                text=processed_text,
                sentiment=label,
                confidence=float(confidence)
            )
            
            return JsonResponse({
                'text': processed_text,
                'sentiment': label,
                'confidence': f"{float(confidence) * 100:.2f}%"
            })
        except Exception as e:
            print(f"Error in analyze_feedback: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def analyze_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            file = request.FILES['file']
            if not file.name.endswith('.txt'):
                return JsonResponse({'error': 'Only .txt files are allowed'}, status=400)

            # Đọc nội dung file
            content = file.read().decode('utf-8')
            lines = [line.strip() for line in content.split('\n') if line.strip()]

            results = []
            for text in lines:
                if not text:
                    continue

                # Xử lý từ viết tắt
                processed_text = acronym.Solve_Acr(text)
                # Dự đoán sentiment
                label, confidence = model.Predict(processed_text)
                
                # Lưu vào database
                feedback = Feedback.objects.create(
                    text=processed_text,
                    sentiment=label,
                    confidence=float(confidence)
                )
                
                results.append({
                    'text': processed_text,
                    'sentiment': label,
                    'confidence': f"{float(confidence) * 100:.2f}%"
                })
            
            return JsonResponse(results, safe=False)
        except Exception as e:
            print(f"Error in analyze_file: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
