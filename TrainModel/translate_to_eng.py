import pandas as pd
from googletrans import Translator
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from requests.exceptions import RequestException

# Đảm bảo tính nhất quán trong phát hiện ngôn ngữ
DetectorFactory.seed = 0

# Khởi tạo Translator
translator = Translator()

# Đọc file CSV và tạo file CSV mới để ghi
input_file = "data_topcv.csv"
output_file = "data.csv"

# Kích thước của mỗi phần (số dòng mỗi chunk)
chunk_size = 100

# Tạo một danh sách để chứa các DataFrame nhỏ
data_frames = []

# Đọc file CSV theo từng phần
reader = pd.read_csv(input_file, iterator=True, chunksize=chunk_size)

for chunk in reader:
    chunk_data_frames = []

    for index, row in chunk.iterrows():
        try:
            description = row['description']
            # Dịch nếu cần
            if detect(description) == 'vi':
                try:
                    translated_text = translator.translate(description, src='vi', dest='en').text
                except RequestException as e:
                    print(f"Lỗi khi kết nối đến dịch vụ dịch thuật: {e}")
                    translated_text = description  # Giữ nguyên nếu không thể dịch
            else:
                translated_text = description

            # Tạo DataFrame cho dòng đã dịch (chỉ giữ cột dịch)
            translated_row = pd.DataFrame({
                'description_translated': [translated_text]
            })

            # Thêm DataFrame vào danh sách của chunk hiện tại
            chunk_data_frames.append(translated_row)

        except LangDetectException:
            print(f"Lỗi phát hiện ngôn ngữ với dòng: {row['description']}")
            continue
        except Exception as e:
            print(f"Lỗi khi dịch hoặc ghi dữ liệu: {e}")
            continue

    # Kết hợp tất cả các DataFrame của chunk hiện tại và thêm vào danh sách tổng
    if chunk_data_frames:
        chunk_df = pd.concat(chunk_data_frames, ignore_index=True)
        data_frames.append(chunk_df)

# Kết hợp tất cả các DataFrame và ghi vào file CSV
if data_frames:
    result_df = pd.concat(data_frames, ignore_index=True)
    result_df.to_csv(output_file, index=False)
    print(f"Hoàn tất dịch và ghi dữ liệu vào {output_file}")
else:
    print("Không có dữ liệu để ghi.")
