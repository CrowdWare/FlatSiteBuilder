rem this only works on Windows
rem adjust the path for binarycreator
rem change version number for executable in this file
rem change the version in config/config.xml
rem change the ReleaseDate in packages/.../meta/package.xml 


pyside6-rcc main.qrc -o main_rc.py
pyside6-rcc resources.qrc -o resources.py
pyside6-rcc plugins/carousel.qrc -o plugins/carousel_rc.py
pyside6-rcc plugins/imageeditor.qrc -o plugins/imageeditor_rc.py
pyside6-rcc plugins/revolution.qrc -o plugins/revolution_rc.py
pyside6-rcc plugins/texteditor.qrc -o plugins/texteditor_rc.py
pyside6-rcc plugins/github.qrc -o plugins/github_rc.py
pyside6-rcc plugins/shopify.qrc -o plugins/shopify_rc.py
pyside6-rcc plugins/markdowneditor.qrc -o plugins/markdowneditor_rc.py
pyside6-rcc plugins/wasm.qrc -o plugins/wasm_rc.py

C:\Qt\6.4.2\mingw_64\bin\lrelease translation\FlatSiteBuilder_de.ts

rmdir dist\main /s /q
rmdir packages\at.crowdware.FlatSiteBuilder\data /s /q

pyinstaller -w main.py
mkdir packages\at.crowdware.FlatSiteBuilder\data
mkdir packages\at.crowdware.FlatSiteBuilder\data\plugins
mkdir packages\at.crowdware.FlatSiteBuilder\data\themes
mkdir packages\at.crowdware.FlatSiteBuilder\data\sources
mkdir packages\at.crowdware.FlatSiteBuilder\data\translation
mkdir packages\at.crowdware.FlatSiteBuilder\data\icon
xcopy dist\main\*.* packages\at.crowdware.FlatSiteBuilder\data /E /H /Y
xcopy plugins\*.py packages\at.crowdware.FlatSiteBuilder\data\plugins /E /H /Y
xcopy themes\*.* packages\at.crowdware.FlatSiteBuilder\data\themes /E /H /Y
copy translation\FlatSiteBuilder_de.qm packages\at.crowdware.FlatSiteBuilder\data\translation
copy images\icon_128.ico packages\at.crowdware.FlatSiteBuilder\data\icon
copy images\icon_128.png packages\at.crowdware.FlatSiteBuilder\data\icon


move packages\at.crowdware.FlatSiteBuilder\data\main.exe packages\at.crowdware.FlatSiteBuilder\data\FlatSiteBuilder.exe
C:\Qt\Tools\QtInstallerFramework\3.2.2\bin\binarycreator -f -c config/config.xml -p packages FlatSiteBuilder-Windows-2.3.0.Setup