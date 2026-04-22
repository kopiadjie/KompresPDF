@echo off
setlocal
cd /d %~dp0
cd ..

echo Mengumpulkan file Ghostscript dan membuild aplikasi PDF Compressor...
echo Ini mungkin memakan waktu agak lama karena kami membungkus Ghostscript (sekitar ~60MB) ke dalam .exe.
echo Mohon tunggu...

pyinstaller --noconsole --onefile ^
  --name "kompres pedeep" ^
  --icon "assets\app_icon.ico" ^
  --distpath "dist" ^
  --workpath "packaging\build" ^
  --specpath "packaging" ^
  --add-data "C:\Program Files (x86)\gs\gs10.07.0\bin;gs\bin" ^
  --add-data "C:\Program Files (x86)\gs\gs10.07.0\lib;gs\lib" ^
  --add-data "C:\Program Files (x86)\gs\gs10.07.0\Resource;gs\Resource" ^
  --add-data "C:\Program Files (x86)\gs\gs10.07.0\iccprofiles;gs\iccprofiles" ^
  --add-data "assets;assets" ^
  src\main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo BUILD SUKSES! 
    echo File aplikasi Anda (kompres pedeep.exe) telah berhasil dibuat dan diletakkan di dalam folder dist.
) else (
    echo.
    echo BUILD GAGAL! Periksa pesan error di atas.
)

pause
endlocal
