from flask import Flask, request, send_file, render_template
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return 'Error: No image provided', 400

    image_file = request.files['image']
    background_file = request.files.get('background')  # Используйте .get для избежания KeyError

    # Удаление фона из изображения
    image_bytes = remove(image_file.read())
    processed_image = Image.open(io.BytesIO(image_bytes)).convert('RGBA')

    if background_file:
        # Если файл фона предоставлен, наложите его
        background = Image.open(background_file).convert('RGBA').resize(processed_image.size)
        final_image = Image.new('RGBA', processed_image.size)
        final_image.paste(background, (0,0))
        final_image.paste(processed_image, (0,0), processed_image)
    else:
        # Иначе, просто используйте обработанное изображение как конечный результат
        final_image = processed_image

    # Сохранение и отправка конечного изображения
    final_image_io = io.BytesIO()
    final_image.save(final_image_io, format='PNG')
    final_image_io.seek(0)

    return send_file(final_image_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)