@echo off
REM Python 가상환경 생성
python -m venv venv
call venv\Scripts\activate

REM Python 라이브러리 설치
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM React 프로젝트 패키지 설치
echo Installing React dependencies...
cd front
npm install
cd ..

REM 서버 실행
echo Starting backend server...
start cmd /k "cd back && call ..\venv\Scripts\activate && python app.py"

echo Starting React frontend...
start cmd /k "cd front && npm start"

echo Starting LLM server...
start cmd /k "cd src && call ..\venv\Scripts\activate && python main.py"

echo All servers are starting. Check each terminal window for output.
pause
