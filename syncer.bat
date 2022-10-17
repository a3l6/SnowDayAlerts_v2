@echo off
SETLOCAL

SET PARAM=%~1
SET ARG=%~2
IF "%PARAM%" == "--save" (
    git add -A
    git commit -m"%ARG%"
    git push origin main
) ELSE IF "%PARAM%" == "--sync" (
    IF "%ARG%" == "-h" (
        git fetch --all
        git reset --hard origin/main

    ) ELSE IF "%ARG%" == "-s" (
        git fetch --all
        git reset --hard origin/main
    )
)
echo %PARAM%