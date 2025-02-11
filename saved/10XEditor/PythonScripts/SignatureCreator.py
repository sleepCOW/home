import N10X

def _IsFunctionDeclaration(Type: str) -> bool:
    return Type == "MemberFunctionDeclaration" or Type == "FunctionDeclaration"


def _IsFunctionDefinition(Type: str) -> bool:
    return Type == "MemberFunctionDefinition" or Type == "FunctionDefinition"


def _IsCurrentLineFunctionDeclaration():
    CurrentLineText = N10X.Editor.GetCurrentLine()
    X, Y = N10X.Editor.GetCursorPos()

    for i in range(0, len(CurrentLineText)):
        SymbolType = N10X.Editor.GetSymbolType((i, Y))
        if _IsFunctionDeclaration(SymbolType):
            return True
    return False


def __MakeImplementationSignature__(DeclarationLine: str):
    FunctionArgStart = DeclarationLine.find("(")
    FunctionArgEnd = DeclarationLine.rfind(")")
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

    # To allow complex default values like const FVector InVec = FVector( 2.f, 4.f )
    # We need to verify that each splitted part has FunctionArg symbol in it
    # And I actually need to go through indexes rather array of tokens in Args because SymbolType operates based on CursorPos
    FilteredArgs = []
    X, Line = N10X.Editor.GetCursorPos()
    Index = FunctionArgStart + 1
    for Arg in Args:
        ArgLen = len(Arg)
        for i in range(0, ArgLen):
            if N10X.Editor.GetSymbolType((Index + i, Line)) == "FunctionArg":
                FilteredArgs.append(Arg)
                break
        Index += 1  # Account for skipped ',' due to split()
        Index += ArgLen

    # Stupid python that doesn't allow modification in place...
    # So I need to write a bs one liner that is unreadable
    # Remove any default params from arguments and any excessive whitespaces that left.
    FilteredArgs = [Arg.split("=")[0].rstrip() for Arg in FilteredArgs]

    Delimeter = ','
    FilteredArgs = Delimeter.join(FilteredArgs)

    ScopeName = N10X.Editor.GetCurrentScopeName() + "::" if N10X.Editor.GetCurrentScopeName() else ""

    return ReturnType + ScopeName + FunctionName + "(" + FilteredArgs + ")" + FunctionTrailingSpecifiers


# Returns line number (starts counting from 0) and actual string where line is found
# So the real line number is return + 1
# But you want to do any API calls to 10x you need line number that starts counting from zero (returned one)
# So if you want a real line number you need to +1
def _FindLineNumber(LineToFind: str, Text: str):
    i = 0
    for Line in Text.splitlines():
        if LineToFind in Line:
            return i, Line
        i = i + 1

    return -1, None


def _Define(bToggleSourceHeader: bool):
    if not _IsCurrentLineFunctionDeclaration():
        print("Function already defined")
        return

    CurrentLineText = N10X.Editor.GetCurrentLine()

    Signature = __MakeImplementationSignature__(CurrentLineText)
    SourceToPaste = Signature + "\n{\n\n}"

    if bToggleSourceHeader:
        N10X.Editor.ExecuteCommand("CppParser.ToggleSourceHeader")

    PageText: str = N10X.Editor.GetFileText()

    # Check whether function is already defined in the file
    # Remember we could have multiple declarations in the file, so we need to check all of them
    SearchPageTextSlice = PageText
    AccumulatedLineNum = 0
    while True:
        SignatureIndex = SearchPageTextSlice.find(Signature)

        # No more signatures in text
        if SignatureIndex == -1:
            break

        LineNum, Line = _FindLineNumber(Signature, SearchPageTextSlice)
        AccumulatedLineNum += LineNum
        for X in range(0, len(Line)):
            SymType = N10X.Editor.GetSymbolType((X, AccumulatedLineNum))
            if _IsFunctionDefinition(SymType):
                print("Function " + Signature + " already defined")
                N10X.Editor.SetCursorPos((X, AccumulatedLineNum))
                return

        SignatureIndex += len(Line)
        SearchPageTextSlice = SearchPageTextSlice[SignatureIndex:]

    # TODO: Function must be pasted between previous and next function, so order is maintained
    PageText += "\n\n" + SourceToPaste
    N10X.Editor.SetFileText(PageText)

    LineNum, Line = _FindLineNumber(Signature, PageText)
    # Set position to be in the curly brackets so we can start typing right away
    N10X.Editor.SetCursorPos((4, LineNum + 2))


def Define():
    FileName = N10X.Editor.GetCurrentFilename()
    Extension = FileName.split('.')[-1]

    # If we happen to call define when we are in "Source" file we defenetily want it to be defined in current file, so no Toggle Source/Header
    if Extension in ["cpp", "cxx", "c"]:
        _Define(False)
    else:
        _Define(True)


def DefineInCurrentFile():
    _Define(False)
