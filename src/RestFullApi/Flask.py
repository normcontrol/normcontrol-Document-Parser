import json
import os

from flask import Flask, jsonify, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from src.PDF.PDFParser import PDFParser

app = Flask(__name__)

UPLOAD_FOLDER = 'C:\\Users\\Slava\\PycharmProjects\\ODT-Parser\\src\\Files'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'odt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/pdfParse/<path>', methods=['GET'])
# def get_tasks(path):
#     pdfParser = PDFParser()
#     lines = pdfParser.getLine(path)
#     space = pdfParser.getSpace(lines)
#     listofParagraph = pdfParser.getParagraph(lines, space)

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл
        if len(request.files) == 0:
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю
            flash('Не могу прочитать файл')
            return "BAD"
        file = request.files.get("file")
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return "BAD"
        if file and allowed_file(file.filename):
            pdfParser = PDFParser()
            lines, listOfTable = pdfParser.getLine(file)
            space = pdfParser.getSpace(lines)
            pdfParser.getParagraph(lines, space, listOfTable)
            json = pdfParser.document.createJsonToDB()
            # response = app.response_class(
            #     response=json,
            #     status=200,
            #     mimetype='application/json'
            # )
            import requests
            url = 'http://localhost:8001/clasify'
            x = requests.post(url, json=json)
            return json
    return "Bad"

if __name__ == '__main__':
    app.run(debug=True)