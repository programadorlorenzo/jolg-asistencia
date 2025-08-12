[Setup]
AppName=Asistencia JOLG
AppVersion=1.0.0
AppPublisher=CONSORCIO LORENZO
AppPublisherURL=https://consorciolorenzo.com
AppSupportURL=https://consorciolorenzo.com/soporte
AppUpdatesURL=https://consorciolorenzo.com/actualizaciones
DefaultDirName={autopf}\AsistenciaJOLG
DefaultGroupName=Asistencia JOLG
AllowNoIcons=yes
LicenseFile=
OutputDir=setup_output
OutputBaseFilename=AsistenciaJOLG_Setup_v1.0.0
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\AsistenciaJOLG.exe

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "startmenu"; Description: "Crear acceso directo en el menú de inicio"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checked

[Files]
Source: "distribucion\AsistenciaJOLG.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "distribucion\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "distribucion\fotos\*"; DestDir: "{app}\fotos"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "distribucion\temp\*"; DestDir: "{app}\temp"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Asistencia JOLG"; Filename: "{app}\AsistenciaJOLG.exe"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,Asistencia JOLG}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Asistencia JOLG"; Filename: "{app}\AsistenciaJOLG.exe"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Asistencia JOLG"; Filename: "{app}\AsistenciaJOLG.exe"; WorkingDir: "{app}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\AsistenciaJOLG.exe"; Description: "{cm:LaunchProgram,Asistencia JOLG}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\fotos"
Type: filesandordirs; Name: "{app}\temp"
Type: filesandordirs; Name: "{app}\asistencia_local.json"

[Messages]
spanish.WelcomeLabel1=Bienvenido al Asistente de Instalación de [name]
spanish.WelcomeLabel2=Este programa instalará [name/ver] en su equipo.%n%nEste sistema permite registrar asistencia de personal mediante captura de fotos y conexión con servidor remoto.%n%nSe recomienda cerrar todas las demás aplicaciones antes de continuar.
spanish.ClickNext=Haga clic en Siguiente para continuar.
spanish.BeveledLabel=Sistema de Asistencia para Personal - CONSORCIO LORENZO

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Crear carpetas adicionales si no existen
    if not DirExists(ExpandConstant('{app}\fotos')) then
      CreateDir(ExpandConstant('{app}\fotos'));
    if not DirExists(ExpandConstant('{app}\temp')) then
      CreateDir(ExpandConstant('{app}\temp'));
  end;
end;
