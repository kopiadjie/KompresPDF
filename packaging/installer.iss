[Setup]
; Informasi umum tentang aplikasi Anda
AppName=Kompres Pedeep
AppVersion=1.0
AppPublisher=Pedeep Creator
DefaultDirName={autopf}\Kompres Pedeep
DefaultGroupName=Kompres Pedeep

; Tempat file installer Setup.exe akan disimpan setelah proses kompilasi Inno Setup selesai
OutputDir=..\dist
OutputBaseFilename=Setup_Kompres_Pedeep

; Ikon untuk file installer
SetupIconFile=..\assets\app_icon.ico

; Konfigurasi kompresi agar ukuran installer lebih kecil
Compression=lzma
SolidCompression=yes

; Ikon uninstall yang akan muncul di Control Panel
UninstallDisplayIcon={app}\kompres pedeep.exe

[Files]
; Mengambil file .exe yang sudah Anda buat dari folder dist lalu memasukkannya ke direktori instalasi {app} (yaitu Program Files)
Source: "..\dist\kompres pedeep.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Membuat shortcut di Start Menu
Name: "{group}\Kompres Pedeep"; Filename: "{app}\kompres pedeep.exe"
; Membuat shortcut di Desktop
Name: "{autodesktop}\Kompres Pedeep"; Filename: "{app}\kompres pedeep.exe"

[Run]
; Menyediakan opsi "Run application" setelah proses install The Setup selesai
Filename: "{app}\kompres pedeep.exe"; Description: "Jalankan Kompres Pedeep"; Flags: nowait postinstall skipifsilent
