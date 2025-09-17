:: 获取日期时间
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do (
    set mydate=%%a-%%b-%%c
)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set mytime=%%a-%%b
)

set commitmsg=%mydate%_%mytime%

echo ================================
echo 正在提交：%commitmsg%
echo ================================

git add .
git commit -m "%commitmsg%"
git push

pause
