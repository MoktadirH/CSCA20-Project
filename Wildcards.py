def skip(turn_index, direction):
    if direction == 1:
        turn_index += 1
    else:
        turn_index -= 1
    return turn_index
def reverse(direction):
    #positive=negative and negative=positve
    #siwtches the direction
    return direction * -1
