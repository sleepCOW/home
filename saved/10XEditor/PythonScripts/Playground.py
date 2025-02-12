import N10X

def GetSymbolType():
    MousePos = N10X.Editor.GetCursorPos()
    print(N10X.Editor.GetSymbolType(MousePos))

def GetPreprocessedLine():
    print(N10X.Editor.GetPreprocessedLine())


def GetSymbolDefinition():
    MousePos = N10X.Editor.GetCursorPos()
    print(N10X.Editor.GetSymbolDefinition(MousePos))


# class SourceCodeLine:
#     def __init__(self, Line: str, LineNum: int):
#         self.Head = SourceCodePart(Line, 0, len(Line), LineNum, None)
#         self.LineNum = LineNum
#
#     @classmethod
#     def FromCurrentLine(cls):
#         X, LineNum = N10X.Editor.GetCursorPos()
#         CurrentLine = N10X.Editor.GetCurrentLine()
#         return __class__(CurrentLine, LineNum)
#
#     def RemoveAll(self, SymbolTypeToRemove: str):
#         # Find start of symbol to remove
#         # Find end of symbol to remove
#         # Split existing part into 2 parts
#         #
#         for Part in self:
#             Part.RemoveAll(SymbolTypeToRemove)
#         print(f'Result of RemovAll = {str(self)}')
#         return self
#
#     def __str__(self):
#         ResultStr = ""
#         Node = self.Head
#         while Node is not None:
#             ResultStr = ResultStr + Node.__str__()
#             Node = Node.Next
#         return ResultStr
#
#     def __iter__(self):
#         self.IterNode = self.Head
#         return self
#
#     def __next__(self):
#         if self.IterNode is None:
#             raise StopIteration
#
#         Node = self.IterNode
#         self.IterNode = self.IterNode.Next
#         return Node
#
#
# class SourceCodePart:
#     def __init__(self, sourceCode: str, Start: int, End: int, LineNum: int, Next):
#         self.Line = sourceCode
#         self.Start = Start
#         self.End = End
#         self.LineNum = LineNum
#         self.Next = Next
#
#     # Returns start index of first occurrence of given symbol
#     # Return -1 if nothing found
#     def FindSymbol(self, SymbolTypeToFind: str, StartPos: int = -1, EndPos: int = -1):
#         print(f'[FindSymbol] SymbolTypeToFind = {SymbolTypeToFind} StartPos = {StartPos} EndPos = {EndPos}')
#         if StartPos == -1:
#             StartPos = self.Start
#         if EndPos == -1:
#             EndPos = self.End
#
#         for i in range(StartPos, EndPos):
#             SymbolType = N10X.Editor.GetSymbolType((i, self.LineNum))
#             if SymbolType == SymbolTypeToFind:
#                 #print(self.Line[self._PosToStrIndex(i)])
#                 return i
#         return -1
#
#     def FindSymbolRange(self, SymbolTypeToFind: str, StartPos: int = -1, EndPos: int = -1):
#         print(f'[FindSymbolRange] SymbolTypeToFind = {SymbolTypeToFind} StartPos = {StartPos} EndPos = {EndPos}')
#         if StartPos == -1:
#             StartPos = self.Start
#         if EndPos == -1:
#             EndPos = self.End
#
#         FoundStart = self.FindSymbol(SymbolTypeToFind, StartPos, EndPos)
#
#         if FoundStart != -1:
#             for i in range(FoundStart + 1, EndPos):
#                 CurrentSymbolType = N10X.Editor.GetSymbolType((i, self.LineNum))
#                 if CurrentSymbolType != SymbolTypeToFind:
#                     return FoundStart, i
#
#         return FoundStart, -1
#
#     def _PosToStrIndex(self, Index: int):
#         return Index - self.Start
#
#     def RemoveAll(self, SymbolTypeToRemove: str):
#         print('[RemoveAll]')
#         # Find start of symbol to remove
#         # Find end of symbol to remove
#         # Split existing part into 2 parts
#         # Call Remove all for the second part
#         Start, End = self.FindSymbolRange(SymbolTypeToRemove)
#         print(f'Removed part = {self.Line[self._PosToStrIndex(Start):self._PosToStrIndex(End)]}')
#         print(f'removed start = {Start}, end = {End}')
#         if Start == -1:
#             return
#
#         # Split into 2 parts omitting the middle wrong one
#
#         print("---SHIT---")
#         # TODO: FIX INCORRECT SPLIT OF LINE
#         NewNext = SourceCodePart(self.Line[self._PosToStrIndex(End):self._PosToStrIndex(self.End)], End, self.End, self.LineNum, self.Next)
#
#         self.Next = NewNext
#         # Now fix first part
#         self.Line = self.Line[0:self._PosToStrIndex(Start)]
#         #self.Start =
#         self.End = Start
#         print(f'Left part = {str(self)}')
#         print(f'Right part = {str(NewNext)}')
#
#         NewNext.RemoveAll(SymbolTypeToRemove)
#
#     def __str__(self):
#         return self.Line
#
#     def __iter__(self):
#         return SourceCodePartIterator(self)
#
#
# class SourceCodePartIterator:
#     def __init__(self, InSourceCodePart):
#         self.SourceCodePart = InSourceCodePart
#         self.Index = InSourceCodePart.Start
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self.Index >= self.SourceCodePart.End - 1:
#             raise StopIteration
#
#         Value = N10X.Editor.GetSymbolType((self.Index, self.SourceCodePart.LineNum))
#         self.Index += 1
#         return Value
#
#
# def Filter():
#     CurrentLine = SourceCodeLine.FromCurrentLine()
#
#     CurrentLine.RemoveAll("Define")
#     print('---RESULT---')
#     print(str(CurrentLine))
#
#     for Part in CurrentLine:
#         print(f'Part = {Part.Line}, {Part.Start}, {Part.End}')
#
#
# def Test_Compare(TestName: str, A, B):
#     if A == B:
#         print(f'Test {TestName} PASSED')
#     else:
#         print(f'Test {TestName} FAILED\n {A} != {B}')
#
#
# def LaunchTest():
#     N10X.Editor.OpenFile("a.h")
#
#     CurrentLine = N10X.Editor.GetCurrentLine()
#     CodeLine = SourceCodeLine.FromCurrentLine()
#
#     Test_Compare("Current line equal to constructed SourceCodeLine", str(CodeLine), CurrentLine)
#
#     MainPart = CodeLine.Head
#     Test_Compare("Length can be obtained via End - Start", MainPart.End - MainPart.Start, len(MainPart.Line))