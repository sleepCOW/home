import N10X

def __MakeImplementationSignature__(DeclarationLine: str):
    FunctionArgStart = DeclarationLine.find("(")
    FunctionArgEnd = DeclarationLine.rfind(")")

    # error not a function if couldn't find any () in the line

    FunctionNameStart = DeclarationLine[0:FunctionArgStart].rfind(" ")

    FunctionName = DeclarationLine[0:FunctionArgStart].split()[-1]

    ReturnTypeEnd = DeclarationLine.find(FunctionName)
    ReturnType = DeclarationLine[0:ReturnTypeEnd]
    ReturnType = ReturnType.replace("virtual", "")
    ReturnType = ReturnType.lstrip()

    # Trailing specifiers can include const, override, final,
    # Obviously we don't want implementation for = 0, = default,  = delete
    FunctionTrailingSpecifiers = DeclarationLine[FunctionArgEnd + 1:]
    FunctionTrailingSpecifiers = FunctionTrailingSpecifiers.replace(";", "")
    FunctionTrailingSpecifiers = FunctionTrailingSpecifiers.replace("override", "")
    FunctionTrailingSpecifiers = FunctionTrailingSpecifiers.replace("final", "")
    FunctionTrailingSpecifiers = FunctionTrailingSpecifiers.rstrip()

    # Extract function arguments from selected line
    Args = DeclarationLine[FunctionArgStart + 1:FunctionArgEnd].split(',')

    # Stupid python that doesn't allow modification in place...
    # So I need to write a bs one liner that is unreadable
    # Remove any default params from arguments and any excessive whitespaces that left.
    Args = [Arg.split("=")[0].rstrip() for Arg in Args]

    Delimeter = ','
    Args = Delimeter.join(Args)

    ScopeName = N10X.Editor.GetCurrentScopeName() + "::" if N10X.Editor.GetCurrentScopeName() else ""

    return ReturnType + ScopeName + FunctionName + "(" + Args + ")" + FunctionTrailingSpecifiers

def _FindLineNumber(LineToFind: str, Text: str):
	Index = -1

	i = 0
	for Line in Text.splitlines():
		if LineToFind == Line:
			return i
		i = i + 1

	return Index

# In case user didn't
def _StupidGoTo():
	CurrentLineText = N10X.Editor.GetCurrentLine()
	X, Y = N10X.Editor.GetCursorPos()
	
	for i in range(0, len(CurrentLineText)):
		SymbolType = N10X.Editor.GetSymbolType((i, Y))
		if SymbolType == "MemberFunctionDeclaration":
			N10X.Editor.ExecuteCommand("GotoSymbolDefinition")
			break

def _Define(bDefineInSourceFile : bool):
	ClassName = N10X.Editor.GetCurrentScopeName()
	CurrentLineText = N10X.Editor.GetCurrentLine()

	Signature = __MakeImplementationSignature__(CurrentLineText)
	SourceToPaste = Signature + "\n{\n\n}"

	if bDefineInSourceFile:
		N10X.Editor.ExecuteCommand("CppParser.ToggleSourceHeader")
	
	PageText = N10X.Editor.GetFileText()

	if Signature in PageText:
		# If we found a signature find the line where signature is located, so we can do GoTo
		print("Function " + Signature + " already defined")
		_StupidGoTo()
		#LineNum = _FindLineNumber(Signature, PageText)
		#N10X.Editor.SetCursorY(LineNum)
		return

	# We can't simply use _StupidGoTo because we maybe in another file
	# Attempt to hack using ToggleSourceHeader and StupidGoTo had no success

	PageText += "\n\n" + SourceToPaste
	N10X.Editor.SetFileText(PageText)
	
	# Can simply split and count PageText lines
	LineNum = _FindLineNumber(Signature, PageText)
	# Set position to be in the curly brackets so we can start typing right away
	N10X.Editor.SetCursorPos((4, LineNum + 2))

def Define():
	_Define(True)

def DefineInHeader():
	_Define(False)

def TestCom():
	print(N10X.Editor.GetFileText())
	MousePos = N10X.Editor.GetCursorPos()
	print(MousePos)
	print(N10X.Editor.GetLine(MousePos[1]))


def SymbolType():
	MousePos = N10X.Editor.GetCursorPos()
	print(N10X.Editor.GetSymbolType(MousePos))

def SymbolDefinition():
	MousePos = N10X.Editor.GetCursorPos()
	print(N10X.Editor.GetSymbolDefinition(MousePos))

def OldDefine():
	ClassName = N10X.Editor.GetCurrentScopeName()
	CurrentLineText = N10X.Editor.GetCurrentLine()

	BeforeVariables = CurrentLineText.split("(")[0]

	print(ClassName)
	print(CurrentLineText)
	print(BeforeVariables)
    #print(BeforeVariables)

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

