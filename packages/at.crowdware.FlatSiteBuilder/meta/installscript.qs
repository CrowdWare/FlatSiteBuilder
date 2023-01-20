function Component()
{
    // default constructor
}

Component.prototype.createOperations = function()
{
    // call default implementation to actually install README.txt!
    component.createOperations();

    if (systemInfo.productType === "windows") {
        component.addOperation("CreateShortcut", "@TargetDir@/README.txt", "@StartMenuDir@/README.lnk",
            "workingDirectory=@TargetDir@", "iconPath=%SystemRoot%/system32/SHELL32.dll",
            "iconId=2", "description=Open README file");
    }
}

Component.prototype.createOperations = function()
{
    component.createOperations();
   if (systemInfo.productType === "windows") {
        component.addOperation("CreateShortcut",
            "@TargetDir@/FlatSiteBuilder.exe",
            "@StartMenuDir@/FlatSiteBuilder.lnk",
            "iconPath=@TargetDir@/icon/icon_128.ico", "iconId=0",
            "description=Start FlatSiteBuilder");
    }
} 