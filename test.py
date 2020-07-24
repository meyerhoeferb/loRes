move_mask_dict = {
    'origin': 0b0000000000000000000001111111,
    'dest': 0b0000000000000011111110000000,
    'captured': 0b0000000000111100000000000000,
    'ep': 0b0000000001000000000000000000,  #en passant capture
    'ps': 0b0000000010000000000000000000,  #pawn start
    'promote': 0b0000111100000000000000000000,
    'castle': 0b0001000000000000000000000000,
} #to print x use format(x,'028b')   (prints 28 bits with left padding)

shift_dict = {
    'origin': 0,
    'dest': 7,
    'captured': 14,
    'ep': 18,
    'ps': 19,
    'promote': 23,
    'castle': 24,
}

import logic
PieceType = logic.PieceType
# print(bin(format(move_mask_dict['origin'], '028b')))
print(move_mask_dict['dest'])
test = 0b1111111
test_shift = test << shift_dict['dest']
print(test_shift)
print(PieceType(4).name)
