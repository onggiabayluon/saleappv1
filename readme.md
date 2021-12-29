# Install Dependency
1. For Window

- pip install -r requirements.txt 

2. For Linux 

- pip install -r requirements.txt (Python 2)

- pip3 install -r requirements.txt (Python 3)

# Chạy File bằng cách gõ câu lệnh bên dưới vào command line
Flask run

[Link mở Localhost](http://127.0.0.1:5000/)

# (optional) Config Environtment variables
File .flaskenv đã được config sẵn đến thư mục làm việc gốc là saleapp ( nếu muốn sửa tên thư mục gốc là src thì đồng thời phải sửa lại .flaskenv FLASK_APP=src )

FLASK_APP=saleapp

FLASK_ENV=development

# (optional) run specific file in vscode as __main__
python -m saleapp.models

# (optional) export dependency to requirement.txt
pip freeze > requirements.txt

# (optional) Install Invirontment in vscode 
- py -3 -m venv venv
- Ctrl Shift P => Select interpreter
