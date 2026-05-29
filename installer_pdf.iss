; Inno Setup Script for LAGUDI - PDF Print Manager
; Created by: Eng. Justo Torres
; Company: Lagudis Fresh Food Group

#define MyAppName "Impresion PDFs"
#define MyAppVersion "1.0"
#define MyAppPublisher "Lagudis Fresh Food Group"
#define MyAppURL "https://www.lagudis.com"
#define MyAppExeName "impresion_pdf.exe"
#define MyAppContact "ghost.jgtv@gmail.com"

[Setup]
; Basic app information
AppId={{F3A5B8C2-7D4E-4A6F-9B8C-2E3D4F5A6B7C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppContact={#MyAppContact}

; Installation directories
DefaultDirName={localappdata}\Lagudi\Impresion PDFs
DefaultGroupName=Lagudi\Impresion PDFs
DisableProgramGroupPage=yes

; Output configuration
OutputDir=installer
OutputBaseFilename=ImpresionPDF_Setup_v{#MyAppVersion}
SetupIconFile=lagudi-logo.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compression
Compression=lzma2/max
SolidCompression=yes

; Windows version requirements
MinVersion=10.0
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

; Visual appearance
WizardStyle=modern
DisableWelcomePage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startmenu"; Description: "Create Start Menu shortcut"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Logo and icon files (needed for the app)
Source: "lagudi-logo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "lagudi-logo.ico"; DestDir: "{app}"; Flags: ignoreversion

; User manual (if exists)
Source: "pdf_print_manager\INSTRUCTIONS.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Name: "{group}\Instructions"; Filename: "{app}\INSTRUCTIONS.txt"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional, selected during install)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Option to run the app after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any files created by the app
Type: filesandordirs; Name: "{app}\logs"
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.new"
Type: files; Name: "{app}\update_log.txt"
Type: files; Name: "{app}\PrintLog_*.txt"

[Code]
// Custom code for installation

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create logs folder
    CreateDir(ExpandConstant('{app}\logs'));
  end;
end;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

  // Check if .NET Framework or required components are installed
  // (Add checks here if needed)

  // Check for previous version
  if RegKeyExists(HKEY_CURRENT_USER, 'Software\Lagudi\Impresion PDFs') then
  begin
    if MsgBox('A previous version of PDF Print Manager is installed. Do you want to continue?',
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

function InitializeUninstall(): Boolean;
begin
  Result := True;

  if MsgBox('Do you want to completely remove PDF Print Manager and all of its components?',
            mbConfirmation, MB_YESNO) = IDYES then
  begin
    Result := True;
  end
  else
  begin
    Result := False;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Clean up registry keys
    RegDeleteKeyIncludingSubkeys(HKEY_CURRENT_USER, 'Software\Lagudi\Impresion PDFs');

    // Optional: Remove user data folder
    if MsgBox('Do you want to remove all user settings and data?',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      DelTree(ExpandConstant('{userappdata}\.pdf_print_manager'), True, True, True);
    end;
  end;
end;
