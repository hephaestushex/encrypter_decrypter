#takes in decimal number and turns it into base 4 number as list e.g. 7 = [0, 1, 3]
def conv(inp):
    if not inp:
        return [0, 0, 0]
    digits = []
    while inp:
        digits.append(inp % 4)
        inp //= 4
    while len(digits) != 3:
        digits.append(0)
    return list(reversed(digits))

#takes base 4 number as list and converts it into decimal e.g. [0, 2, 1] = 9
def conv_back(inp):
    inp = list(reversed(inp))
    value = 0
    for x in range(0, len(inp)):
        value+=inp[x]*(4**x)
    return value


#convert int to list
def conv_rkey(rkey):
    key = []
    for x in range(0,3):
        key.append(rkey // 10**x % 10)
    return list(reversed(key))

#initialise dictionary with letters and base 4 values. e.g {'a':[0,0,0]}
key = {}
characters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    '!', '@', '#', '$', '%', '&', '*', '(', ')', '-', '_', '=', '+', 
    '[', ']', '{', '}', ';', ':', ',', '.', '<', '>', '/', '?', '|', ' ', '"'
]

for keyed_character in range(0, len(characters)):
    key[characters[keyed_character]] = conv(keyed_character)

msg = ""
encrypted_message_1 = []
encrypted_message_2 = []
buffermsg = []
final_msg = []
rkey = ""
includekey = False

print("Welcome to the Encrypter and Decrypter Software")
mode = input("What would you like to do? EXIT, ENCRYPT, DECRYPT ")
while mode != "EXIT":
    if mode == "ENCRYPT":
        print("Please enter your message below. Symbols allowed are:")
        print("!, @, #, $, %, ^, &, *, (, ), -, _, =, +, [, ], {, }, ; , :, ',', . , <, >, /, ?, |, ' ', \" ")
        msg = input("Type message here: ")
        msg = msg.lower()
        rkey = (int(input("Enter your encryption key here(3 digits, 0 or 1) e.g '011'\nWARNING! 000 is no key, and any other value will result in no encryption "))+2000)
        includekey = bool(int(input("Do you wish to include the key with encrypted message?\nIt is safer not to, but you will have to specify the key to decrypt.\nIncluding it will do so automatically (0 for No, 1 for Yes): ")))
        rkey = conv_rkey(rkey)

        #Converts each letter in message into base 4 representation
        for letter in range(0, len(msg)):
            encrypted_message_1.append(key[msg[letter]])

        #Takes lists within lists and converts into large list
        for x in range(0, len(encrypted_message_1)):
            for y in range(0, len(encrypted_message_1[x])):
                buffermsg.append(encrypted_message_1[x][y])

        #Swaps around values within large list
        for innerlist in range(0, len(encrypted_message_1)):
            buffer_in_list = []
            for vertex in range(0, len(encrypted_message_1[innerlist])):
                buffer_in_list.append(buffermsg[(vertex*len(encrypted_message_1)+innerlist)])
            encrypted_message_2.append(buffer_in_list)

        #reverses the entire message if the 3rd value in the rkey is equal to 1
        encrypted_message_2 = list(reversed(encrypted_message_2)) if rkey[2] == 1 else encrypted_message_2 if rkey[2] == 0 else encrypted_message_2
        
        #Reverses each char in the message and converts it back from base 4 into a character
        for char in range(0, len(encrypted_message_2)):

            encrypted_message_2[char] = list(reversed(encrypted_message_2[char])) if rkey[(char%2)] != 0 else encrypted_message_2[char] if rkey[char%2] != 1 else encrypted_message_2[char]

            encrypted_message_2[char] = characters[conv_back(encrypted_message_2[char])]

        #Chunk prints final message
        print("Final Message Below")
        if includekey:
            print("%", end="")
            print(characters[conv_back(rkey)],end="")
        for enchar in range(0, len(encrypted_message_2)):
            print(encrypted_message_2[enchar],end="")

        print("")

    elif mode == "DECRYPT":

        msg = input("Enter message here: ")
        msg = list(msg)

        if msg[0] != "%":
            rkey = (int(input("Enter reversing key here. Key must be 3 digits, 0 or 1): "))+2000)
            rkey = conv_rkey(rkey)
        else:

            rkey = key[msg[1]]

            del msg[0]
            del msg[0]


        #Lets convert back to base 4
        for char in range(0, len(msg)):
            
            msg[char] = key[msg[char]]
        

        for inchar in range(0, len(msg)):

            msg[inchar] = list(reversed(msg[inchar])) if rkey[(inchar%2)] != 0 else msg[inchar] if rkey[inchar%2] != 1 else msg[inchar]
        

        msg = list(reversed(msg)) if rkey[2] == 1 else msg if rkey[2] == 0 else msg


        finalmsg = []
        buffermsg=[]

        for k in range(0, len(msg)):
            finalmsg.append([0,0,0])
            for l in range(0, len(msg[k])):
                buffermsg.append(msg[k][l])

        for charlist in range(0, len(msg)):
            for base_4_val in range(0, len(msg[charlist])):
                place_val = (base_4_val*len(msg)+charlist)
                finalmsg[place_val//len(msg[charlist])][place_val%len(msg[charlist])] = buffermsg[charlist*len(msg[charlist])+base_4_val]



        print("Final Message Below")
        for dechar in range(0, len(finalmsg)):
            finalmsg[dechar] = characters[conv_back(finalmsg[dechar])]
            print(finalmsg[dechar],end="")
        print("")

    else:
        print("Unknown input, try again")

    mode = input("What would you like to do? EXIT, ENCRYPT, DECRYPT ")

    


