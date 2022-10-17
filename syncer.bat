@echo off
SETLOCAL

SET PARAM=%~1
SET COMMITMESSAGE=%~2
IF "%PARAM%" == "--save" (
    git add -A
    git commit -m"%COMMITMESSAGE%"
    git push origin main
) ELSE IF "%PARAM%" == "--sync" (
    git fetch --all
    git reset --hard origin/main
)
echo %PARAM%