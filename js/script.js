// Converts a decimal number to base-4 as a list (e.g., 7 -> [0, 1, 3])
function conv(inp) {
    if (!inp) return [0, 0, 0];
    const digits = [];
    while (inp) {
        digits.push(inp % 4);
        inp = Math.floor(inp / 4);
    }
    while (digits.length < 3) {
        digits.push(0);
    }
    return digits.reverse();
}

// Converts a base-4 list to a decimal number (e.g., [0, 2, 1] -> 9)
function convBack(inp) {
    inp = inp.slice().reverse();
    return inp.reduce((value, digit, index) => value + digit * Math.pow(4, index), 0);
}

// Converts an integer to a list of its digits (e.g., 123 -> [1, 2, 3])
function convRKey(rkey) {
    const key = [];
    for (let x = 0; x < 3; x++) {
        key.unshift(Math.floor(rkey / Math.pow(10, x)) % 10);
    }
    return key;
}

// Initialize dictionary with letters and their base-4 values
const characters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '!', '@', '#', '$', '%', '&', '*', '(', ')', '-', '_', '=', '+',
    '[', ']', '{', '}', ';', ':', ',', '.', '<', '>', '/', '?', '|', ' ', '"'
];

const key = {};
characters.forEach((char, index) => {
    key[char] = conv(index);
});

function encrypt(form){
    let msg = form.msg.value;
    let rkey = parseInt(form.rkey.value);
    let inkey = form.inkey.checked;
    console.log(inkey)

    let encryptedMessage1 = [];
    let encryptedMessage2 = [];
    let bufferMsg = [];
    

    
    msg = msg.toLowerCase();
    rkey = convRKey(rkey);

    // Converts each letter in message into base-4 representation
    for (let letter of msg) {
        encryptedMessage1.push(key[letter]);
    }

    // Flattens the lists into a large list
    encryptedMessage1.forEach(innerList => {
        bufferMsg.push(...innerList);
    });

    // Swaps around values within the large list
    for (let i = 0; i < encryptedMessage1.length; i++) {
        const bufferInList = [];
        for (let j = 0; j < encryptedMessage1[i].length; j++) {
            bufferInList.push(bufferMsg[j * encryptedMessage1.length + i]);
        }
        encryptedMessage2.push(bufferInList);
    }

    // Reverses the entire message if the 3rd value in the rkey is 1
    if (rkey[2] === 1) encryptedMessage2.reverse();

    // Reverses each character in the message and converts it back from base-4 into a character
    encryptedMessage2 = encryptedMessage2.map((char, index) => {
        if (rkey[index % 2] !== 0) char.reverse();
        return characters[convBack(char)];
    });

    // Prints the final message
    const finalElement = document.getElementById("finalmsg");
    if (finalElement) {
        let finalMessage = "";
        if (inkey) {
            finalMessage += "%" + characters[convBack(rkey)];
        }
        finalMessage += encryptedMessage2.join("");
        finalElement.innerText = finalMessage;
    }    
}

function decrypt(form){
    let msg = form.msg.value;
    msg = msg.split("");

    let rkey = parseInt(form.rkey.value);
    let finalMsg = [];

    if (msg[0] !== "%") {
        rkey = convRKey(rkey);
    } else {
        rkey = key[msg[1]];
        msg.splice(0, 2);
    }

    // Convert back to base-4
    msg = msg.map(char => key[char]);

    msg = msg.map((char, index) => {
        if (rkey[index % 2] !== 0) char.reverse();
        return char;
    });

    if (rkey[2] === 1) msg.reverse();

    finalMsg = Array.from({ length: msg.length }, () => [0, 0, 0]);
    bufferMsg = [].concat(...msg);

    for (let i = 0; i < msg.length; i++) {
        for (let j = 0; j < msg[i].length; j++) {
            const placeVal = j * msg.length + i;
            finalMsg[Math.floor(placeVal / msg[i].length)][placeVal % msg[i].length] = bufferMsg[i * msg[i].length + j];
        }
    }

    const finalElement = document.getElementById("finalmsg");
    if (finalElement) {
        finalElement.innerText = finalMsg.map(char => characters[convBack(char)]).join("");
    }
}




