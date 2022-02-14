

import binascii

from .TokenizerBase import TokenizerAction as TA
from .TokenizerBase import TokenizerPattern as TP
from .TokenizerBase import TokenizerBase, TokenizingTable



class TokenizerStrict(TokenizerBase):

	def __init__(self):
		tables = self.createTables(3)
		tableNRM, tableINSTRING2, tableINSTRING2MASKED = tables

		tableNRM.addPatternRow(TP.exactChar("\n"),										[ TA.advance() ])
		tableNRM.addPatternRow(TP.anyOfTheseChars(" \t"),								[ TA.advance() ])
		tableNRM.addPatternRow(TP.regEx(r"[+-]?0?\.[0-9]+([Ee][+-]?[1-9][0-9]+)?"),		[ TA.emitElement("f"), TA.advance() ])
		tableNRM.addPatternRow(TP.regEx(r"[+-]?[1-9][0-9]*\.[0-9]+([Ee][+-]?[0-9]+)?"),	[ TA.emitElement("f"), TA.advance() ])
		tableNRM.addPatternRow(TP.regEx(r"[+-]?[1-9][0-9]*([Ee][+-]?[0-9]+)"),			[ TA.emitElement("f"), TA.advance() ])
		tableNRM.addPatternRow(TP.regEx(r"[+-]?[1-9][0-9]*"),							[ TA.emitElement("i"), TA.advance() ])
		tableNRM.addPatternRow(TP.regEx(r"[+-]?0"),										[ TA.emitElement("i"), TA.advance() ])
		tableNRM.addPatternRow(TP.regEx(r"[a-zA-Z\._][a-zA-Z0-9\._-]*"),				[ TA.emitElement("w"), TA.advance() ])
		tableNRM.addPatternRow(TP.exactChar("\""),										[ TA.advance(), TA.beginBuffer(), TA.switchMode(tableINSTRING2.tableID) ])
		tableNRM.addPatternRow(TP.anyOfTheseChars("_-+*~#'`!§$%&/()[]{}=?\\,.;:<>|"),	[ TA.emitElement("d"), TA.advance() ])
		tableNRM.setOther([ TA.error("T0003", "Syntax error! Failed to tokenize a character sequence!", 1) ])
		tableNRM.setEOS([ TA.emitElement("eos") ])

		tableINSTRING2.addPatternRow(TP.exactChar("\""),								[ TA.emitBuffer("s"), TA.advance(), TA.switchMode(tableNRM.tableID) ])
		tableINSTRING2.addPatternRow(TP.anyOfTheseChars("\\"),							[ TA.advance(), TA.switchMode(tableINSTRING2MASKED.tableID) ])
		tableINSTRING2.setOther([ TA.appendElementToBuffer(), TA.advance() ])
		tableINSTRING2.setEOS([ TA.error("T0002", "Syntax error! Unexpected EOS in string!", 2) ])

		tableINSTRING2MASKED.addPatternRow(TP.regEx(r"u[0-9a-fA-F]{4}"),				[ TA.appendElementToBuffer(self.__convert4HexToUnicode), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.addPatternRow(TP.exactChar("\\"),							[ TA.appendTextToBuffer("\\"), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.addPatternRow(TP.exactChar("n"),							[ TA.appendTextToBuffer("\n"), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.addPatternRow(TP.exactChar("r"),							[ TA.appendTextToBuffer("\r"), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.addPatternRow(TP.exactChar("t"),							[ TA.appendTextToBuffer("\t"), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.addPatternRow(TP.exactChar("f"),							[ TA.appendTextToBuffer("\f"), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.addPatternRow(TP.exactChar("b"),							[ TA.appendTextToBuffer("\b"), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.addPatternRow(TP.exactChar("/"),							[ TA.appendTextToBuffer("/"), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.addPatternRow(TP.exactChar("\""),							[ TA.appendTextToBuffer("\""), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.setOther([ TA.appendElementToBuffer(), TA.advance(), TA.switchMode(tableINSTRING2.tableID) ])
		tableINSTRING2MASKED.setEOS([ TA.error("T0002", "Syntax error! Unexpected EOS in string!", 4) ])

		super().__init__(tables)
	#

	def __convert4HexToUnicode(self, text):
		binData = binascii.unhexlify(text[1:])
		# NOTE: truncating the data has been removed as this is erroneous
		return binData.decode("utf-16-be")
	#

#








