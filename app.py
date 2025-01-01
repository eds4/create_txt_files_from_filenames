from flask import Flask, request, render_template, send_file
import os

app = Flask(__name__)

# 建立首頁
@app.route('/')
def index():
    return render_template('index.html')  # 返回首頁 HTML

# 上傳檔案並處理
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # 儲存檔案到本地
        filepath = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(filepath)

        # 進行處理（例如轉換檔名並生成 txt）
        output_folder = process_files(filepath)

        # 壓縮並提供下載
        zip_path = create_zip(output_folder)
        return send_file(zip_path, as_attachment=True)
    return 'No file uploaded!'

def process_files(filepath):
    # 你的檔案處理邏輯
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)
    # 範例：生成對應的 TXT 檔案
    with open(filepath, 'r') as f:
        content = f.read()
        with open(os.path.join(output_folder, 'example.txt'), 'w') as out:
            out.write(content)
    return output_folder

def create_zip(folder):
    # 壓縮目錄
    import shutil
    zip_path = 'output.zip'
    shutil.make_archive('output', 'zip', folder)
    return zip_path

if __name__ == '__main__':
    app.run(debug=True)
