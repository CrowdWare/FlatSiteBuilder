# this only works on Linux
# adjust the path for binarycreator
# change version number for executable in this file
# change the version in config/config.xml
# change the ReleaseDate in packages/.../meta/package.xml 

pyside6-rcc main.qrc -o main_rc.py
pyside6-rcc resources.qrc -o resources.py
pyside6-rcc plugins/carousel.qrc -o plugins/carousel_rc.py
pyside6-rcc plugins/imageeditor.qrc -o plugins/imageeditor_rc.py
pyside6-rcc plugins/revolution.qrc -o plugins/revolution_rc.py
pyside6-rcc plugins/texteditor.qrc -o plugins/texteditor_rc.py
pyside6-rcc plugins/github.qrc -o plugins/github_rc.py
pyside6-rcc plugins/shopify.qrc -o plugins/shopify_rc.py

/home/art/Qt/6.2.1/gcc_64/bin/lrelease translation/FlatSiteBuilder_de.ts

rm -r dist/*
rm -r packages/at.crowdware.flatsitebuilder/data/*
pyinstaller main.py
mkdir packages/at.crowdware.flatsitebuilder/data
mkdir packages/at.crowdware.flatsitebuilder/data/plugins
mkdir packages/at.crowdware.flatsitebuilder/data/themes
mkdir packages/at.crowdware.flatsitebuilder/data/sources
mkdir packages/at.crowdware.flatsitebuilder/data/translation
mkdir packages/at.crowdware.flatsitebuilder/data/icon
cp -r dist/main/* packages/at.crowdware.flatsitebuilder/data
cp plugins/*.py packages/at.crowdware.flatsitebuilder/data/plugins
cp -r themes/* packages/at.crowdware.flatsitebuilder/data/themes

cp translation/FlatSiteBuilder_de.qm packages/at.crowdware.flatsitebuilder/data/translation
cp images/icon_128.ico packages/at.crowdware.flatsitebuilder/data/icon
cp images/icon_128.png packages/at.crowdware.flatsitebuilder/data/icon

mv packages/at.crowdware.flatsitebuilder/data/main packages/at.crowdware.flatsitebuilder/data/FlatSiteBuilder
/home/art/Qt/Tools/QtInstallerFramework/4.2/bin/binarycreator -f -c config/config.xml -p packages FlatSiteBuilder-Linux-2.1.9.Setup