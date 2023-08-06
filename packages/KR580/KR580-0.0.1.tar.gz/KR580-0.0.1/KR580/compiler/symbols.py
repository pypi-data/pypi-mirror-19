rg_names = ('A', 'B', 'C', 'D', 'E', 'H', 'L', 'M', 'SP')
cmds = ('NOP', 'LXI', 'SHLD', 'STAX', 'STA', 'INX', 'INR', 'DCR', 'MVI', 'RLC',
        'RAL', 'DAA', 'STC', 'DAD', 'LDAX', 'LHLD', 'LDA', 'DCX', 'RRC', 'RAR',
        'CMA', 'CMC', 'RIM', 'SIM', 'MOV', 'ADD', 'SUB', 'ANA', 'ORA', 'ADC',
        'SBB', 'XRA', 'CMP', 'RNZ', 'RNC', 'RPO', 'RP', 'POP', 'JNZ', 'JNC',
        'JPO', 'JP', 'JMP', 'OUT', 'XTHL', 'DI', 'CNZ', 'CNC', 'CPO', 'CP',
        'PUSH', 'ADI', 'SUI', 'ANI', 'ORI', 'RST', 'RZ', 'RC', 'RPE', 'RM',
        'RET', 'PCHL', 'SPHL', 'JZ', 'JC', 'JPE', 'JM', 'IN', 'XCHG', 'EI',
        'CZ', 'CC', 'CPE', 'CM', 'CALL', 'ACI', 'SBI', 'XRI', 'CPI', 'HLT')

tokens = ('WORD', 'ID', 'COLON', 'RG_NAME', 'CMD', 'DECLARATION')
