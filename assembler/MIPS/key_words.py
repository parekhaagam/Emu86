from .arithmetic import Add, Sub, Addi, Mult, Div
from .arithmetic import Andf, Andi, Orf, Ori, Xor, Nor, Sll, Srl
from .arithmetic import Mflo, Mfhi
from .data_mov import Load, Store
from .control_flow import Slt, Slti, Beq, Bne, Jmp, Jal
from assembler.tokens import DataType

key_words = {
	# data types
	'.BYTE': DataType('DB'),
    '.WORD': DataType('DW'),

    # data movement:
	'LW': Load('LW'),
	'SW': Store('SW'),

	# arithmetic and logic
	'ADD': Add('ADD'),
	'ADDI': Addi('ADDI'),
	'SUB': Sub('SUB'),
	'MULT': Mult('MULT'),
	'DIV': Div('DIV'),
	'MFLO': Mflo('MFLO'),
	'MFHI': Mfhi('MFHI'),
	'AND': Andf('AND'),
	'ANDI': Andi('ANDI'),
	'OR': Orf('OR'),
	'ORI': Ori('ORI'),
	'XOR': Xor('XOR'),
	'NOR': Nor('NOR'),
	'SLL': Sll('SLL'),
	'SRL': Srl('SRL'),

	#control 
	'SLT': Slt('SLT'),
	'SLTI': Slti('SLTI'),
	'BEQ': Beq('BEQ'),
	'BNE': Bne('BNE'),
	'J': Jmp('J'),
	'JAL': Jal('JAL')
}

op_func_codes = {
	# R-format
	'ADD': ('000000', '100000'),
	'SUB': ('000000', '100010'),
	'MULT': ('000000', '011000'),
	'DIV': ('000000', '011010'),
	'MFLO': ('000000', '010010'),
	'MFHI': ('000000', '010000'),
	'AND': ('000000', '100100'),
	'OR': ('000000', '100101'),
	'XOR': ('000000', '100110'),
	'NOR': ('000000', '100111'),
	'SLL': ('000000', '000000'),
	'SRL': ('000000', '000010'),
	'SLT': ('000000', '101010'),

    # I-format
	'LW': '100011',
	'SW': '101011',
	'ADDI': '001000',
	'ANDI': '001100',
	'ORI': '001101',
	'SLTI': '001010',
	'BEQ': '000100',
	'BNE': '000101',

	#J-format
	'J': '000010',
	'JAL': '000011'
}
