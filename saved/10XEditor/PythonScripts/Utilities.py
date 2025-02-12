import N10X


class SourceCodeLine:
    """
    Abstraction over a part of source code, currently can represent only substring of a single line
        but can be extended for multi-line in the future

    Stores position information along with the string, so any API calls with CursorPos can be done with raging
    """

    def __init__(self, Line: str, LineNum: int):
        self.Head = SourceCodePart(Line, 0, len(Line), LineNum, None)

    @classmethod
    def FromCurrentLine(cls):
        """
        Creates a SourceCodeLine instance from the current cursor position in the editor.

        :return: A new SourceCodeLine instance based on the current editor state.
        """
        X, LineNum = N10X.Editor.GetCursorPos()
        CurrentLine = N10X.Editor.GetCurrentLine()
        return __class__(CurrentLine, LineNum)

    def RemoveAll(self, SymbolTypeToRemove: str):
        """
        Removes all occurrences of a specific symbol type from the source code line.

        :param SymbolTypeToRemove: The type of symbol to remove. Examples "Definition", "FunctionDeclaration", etc.
            see GetSymbolType() for all possible types
        :return: The modified SourceCodeLine instance. for chained calls
        """
        for Part in self:
            Part.RemoveAll(SymbolTypeToRemove)
        return self

    def __str__(self):
        """
        Converts the source code line to a string representation.

        :return: The concatenated string representation of all parts.
        """
        ResultStr = ""
        Node = self.Head
        while Node is not None:
            ResultStr = ResultStr + Node.__str__()
            Node = Node.Next
        return ResultStr

    def __iter__(self):
        """
        Initializes an iterator over the source code parts.
        """
        self.IterNode = self.Head
        return self

    def __next__(self):
        if self.IterNode is None:
            raise StopIteration

        Node = self.IterNode
        self.IterNode = self.IterNode.Next
        return Node


class SourceCodePart:
    """
    Represents a fragment of a source code line, with start and end cursor positions for easy API calls.
    """

    def __init__(self, sourceCode: str, Start: int, End: int, LineNum: int, Next):
        """
        :param sourceCode: The source code content of the part.
        :param Start: The starting CURSOR index of this part.
        :param End: The ending CURSOR index of this part.
        :param LineNum: The line number where this part belongs.
        :param Next: The next SourceCodePart in the sequence.
        """
        self.Line = sourceCode
        self.Start = Start
        self.End = End
        self.LineNum = LineNum
        self.Next = Next

    def FindSymbol(self, SymbolTypeToFind: str, StartPos: int = -1, EndPos: int = -1):
        """
        Finds the start index of the first occurrence of a given symbol type.

        :param SymbolTypeToFind: The symbol type to search for.
        :param StartPos: The starting CURSOR position for the search (defaults to self.Start).
        :param EndPos: The ending position CURSOR for the search (defaults to self.End).
        :return: The index of the first occurrence, or -1 if not found.
        """
        if StartPos == -1:
            StartPos = self.Start
        if EndPos == -1:
            EndPos = self.End

        # TODO: Support search for multiple parts
        # Imagine for any reason that we have two parts "vir" and "tual" and we want to search for "virtual"
        # Currently no use-case but maybe a problem in the future
        for i in range(StartPos, EndPos):
            SymbolType = N10X.Editor.GetSymbolType((i, self.LineNum))
            if SymbolType == SymbolTypeToFind:
                return i
        return -1

    def FindSymbolRange(self, SymbolTypeToFind: str, StartPos: int = -1, EndPos: int = -1):
        """
        Finds the range (start and end indices) of a given symbol type.

        :param SymbolTypeToFind: The symbol type to search for.
        :param StartPos: The starting CURSOR position for the search.
        :param EndPos: The ending CURSOR position for the search.
        :return: A tuple (start, end) representing the symbol's range, or (-1, -1) if not found.
        """
        if StartPos == -1:
            StartPos = self.Start
        if EndPos == -1:
            EndPos = self.End

        FoundStart = self.FindSymbol(SymbolTypeToFind, StartPos, EndPos)

        if FoundStart != -1:
            for i in range(FoundStart + 1, EndPos):
                CurrentSymbolType = N10X.Editor.GetSymbolType((i, self.LineNum))
                if CurrentSymbolType != SymbolTypeToFind:
                    return FoundStart, i

        return FoundStart, -1

    def _PosToStrIndex(self, Index: int):
        """
        Converts a position in the source code content to an index relative to the part.

        :param Index: The CURSOR index to translate.
        :return: The relative index within the part.
        """
        return Index - self.Start

    def RemoveAll(self, SymbolTypeToRemove: str):
        """
        Removes all occurrences of a specific symbol type from this part.

        :param SymbolTypeToRemove: The symbol type to remove.
        """
        # Find start, end of symbol to remove
        Start, End = self.FindSymbolRange(SymbolTypeToRemove)
        if Start == -1:
            return

        # Split into 2 parts omitting the found middle (containing symbol we want to remove)
        NewNext = SourceCodePart(self.Line[self._PosToStrIndex(End):self._PosToStrIndex(self.End)], End, self.End,
                                 self.LineNum, self.Next)
        self.Next = NewNext

        # Now fix first part end index and content
        self.Line = self.Line[0:self._PosToStrIndex(Start)]
        self.End = Start

        # Remove recursively till we process the whole source line
        NewNext.RemoveAll(SymbolTypeToRemove)

    def __str__(self):
        """
        Converts the SourceCodePart to a string representation.

        :return: The source code content of this part.
        """
        return self.Line

    def __iter__(self):
        return SourceCodePartySymbolTypeIterator(self)


class SourceCodePartySymbolTypeIterator:
    """
    Iterator for SourceCodePart, iterating over its symbol types.
    """

    def __init__(self, InSourceCodePart):
        self.SourceCodePart = InSourceCodePart
        self.Index = InSourceCodePart.Start

    def __iter__(self):
        return self

    def __next__(self):
        if self.Index >= self.SourceCodePart.End - 1:
            raise StopIteration

        Value = N10X.Editor.GetSymbolType((self.Index, self.SourceCodePart.LineNum))
        self.Index += 1
        return Value
