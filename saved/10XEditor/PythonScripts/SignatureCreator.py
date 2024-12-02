import N10X

def Define():
	ClassName = N10X.Editor.GetCurrentScopeName()
	CurrentLineText = N10X.Editor.GetCurrentLine()

	BeforeVariables = CurrentLineText.split("(")[0]
	
	#removing a stupid amount of edge cases
	BeforeVariables = BeforeVariables.replace(";","")
	BeforeVariables = BeforeVariables.replace("virtual", "")
	BeforeVariables = BeforeVariables.replace("override", "")
	BeforeVariables = BeforeVariables.replace("const", "")
	BeforeVariables = BeforeVariables.replace("static", "")

	CurrentLineText = BeforeVariables + "(" + CurrentLineText.split("(")[1]
	CurrentLineText = CurrentLineText.replace(';', '')


	SplitLine = CurrentLineText.split()

	RestOfTheDefinition = ""
	
	for i in range(len(SplitLine)):
		if i == 0:
			continue
		if i == 1:
			RestOfTheDefinition += SplitLine[i]
		else:
			RestOfTheDefinition += " " + SplitLine[i]

	FinalDefinitionNoCurlies = SplitLine[0] + " " + ClassName + "::" + RestOfTheDefinition
	FinalDefinition = FinalDefinitionNoCurlies + "\n{\n\n}"
	ToggleCppHeader()
	
	PageText = N10X.Editor.GetFileText()
	
	if FinalDefinitionNoCurlies in PageText:
		print("Function " + FinalDefinitionNoCurlies + " already defined")
		ToggleCppHeader()
		return

	PageText += "\n\n" + FinalDefinition
	N10X.Editor.SetFileText(PageText)

def ToggleCppHeader():
	FileName = N10X.Editor.ExecuteCommand("CppParser.ToggleSourceHeader")

