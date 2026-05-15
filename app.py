import os
import uuid
from flask import Flask, request, render_template, send_file, jsonify
from report_generator import generate_report, TEMPLATES, DEFAULT_TEMPLATE

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

UPLOAD_FOLDER = '/tmp/hotel_uploads'
OUTPUT_FOLDER = '/tmp/hotel_outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    if 'file' not in request.files:
        return jsonify({'error': 'ไม่พบไฟล์'}), 400

    file = request.files['file']
    hotel_name    = request.form.get('hotel_name', '').strip()
    template_name = request.form.get('template_name', DEFAULT_TEMPLATE).strip()
    if template_name not in TEMPLATES:
        template_name = DEFAULT_TEMPLATE

    if not file.filename:
        return jsonify({'error': 'กรุณาเลือกไฟล์'}), 400
    if not hotel_name:
        return jsonify({'error': 'กรุณากรอกชื่อโรงแรม'}), 400
    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'รองรับเฉพาะไฟล์ .xlsx'}), 400

    # Save uploaded file
    uid = str(uuid.uuid4())
    input_path  = os.path.join(UPLOAD_FOLDER, f'{uid}_input.xlsx')
    output_path = os.path.join(OUTPUT_FOLDER, f'{uid}_report.xlsx')
    file.save(input_path)

    try:
        generate_report(input_path, hotel_name, output_path, template_name=template_name)
    except Exception as e:
        return jsonify({'error': f'เกิดข้อผิดพลาด: {str(e)}'}), 500
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

    safe_name = hotel_name.replace(' ', '_')
    return send_file(
        output_path,
        as_attachment=True,
        download_name=f'report_{safe_name}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
