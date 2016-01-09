import numpy
import sys
from PIL import Image

stop_seq = "///"

num_bits = 8
stripes = 4
red = 0
in_file = "in.bmp"
out_file = "out.bmp"

def convert_char_to_binary(char):
    result = bin(ord(char))[2:]
    result = result.zfill(num_bits)
    return result

def convert_to_two_bits(string):
    return [ string[i * 2: (i * 2) + 2] for i in range(stripes) ]

def string_to_binary(user_string):
    message_binary = []
    length = len(user_string)
    message_binary = map(convert_char_to_binary, user_string)
    return reduce(lambda x,y: x+y, map(convert_to_two_bits, message_binary))

def get_message_binary():
    user_input = raw_input("What's your message?: ")
    message_binary = string_to_binary(user_input)
    message_binary.extend(string_to_binary(stop_seq))
    return message_binary

def insert_message(message_transformed, in_file, out_file):
    image = Image.open(in_file)
    img_arr = numpy.array(image)
    width, height = image.size
    row = 0
    check_image_capicity(message_transformed, img_arr)
    
    while len(message_transformed) > 0:
        for i in range (width):
            if len(message_transformed) == 0:
                break

            binary = bin(img_arr[row][i][red])[2:]
            binary = binary.zfill(num_bits)

            most_sig_bits = binary[:8 - (num_bits // stripes) ]
            new_pixel_value = str(most_sig_bits) + message_transformed.pop(0)
            img_arr[row][i][red] = int(new_pixel_value,2)
        
        row += 1
        if row > height:
            break

    result = Image.fromarray(img_arr)
    result.save(out_file)

def check_image_capicity(message_binary, img_arr):
    try:
        assert( len(message_binary) * stripes < img_arr.size)
    except:
        max_size = (img_arr.size // stripes) - len(stopSeq)
        print "Error:  Message is too long, image has a max capicity of {} characters".format(max_size)
        sys.exit(1)

def fetch_message(img_file, stop_seq_striped):
    message_binary = []
    image = Image.open(img_file)
    width, height = image.size
    img_arr = numpy.array(image)
    row, length = 0, len(stop_seq_striped)
    done_fetching = False
    while not done_fetching:
        if row == height:
            break
        for i in range (width):
            binary = bin(img_arr[row][i][red])[2:]
            least_2_sig_bits = binary[-2].zfill(2)
            message_binary.append(least_2_sig_bits)
            if message_binary[-length:] == stop_seq_striped:
                done_fetching = True
                break
        row += 1
    decode_message(message_binary)

def decode_message(message_binary):
    decoded_message = ""
    while len(message_binary) > 0:
        if len(message_binary) >= stripes:
            temp = ""
            for i in range(stripes):
                temp += message_binary.pop(0)
            decoded_message += chr(int(temp,2))
    print "message: \n{}".format(decoded_message[:-len(stop_seq)])

if __name__=='__main__':
    if len(sys.argv) == 1:
        print "please provide an argument:\n\tencode: to encode a message in test.jpeg\n\tdecode: decode the message in out.bmp"
    elif "encode" in sys.argv:
        message_binary = get_message_binary()
        insert_message(message_binary, in_file, out_file)
    elif "decode" in sys.argv:
        stop_seq_striped = string_to_binary(stop_seq)
        fetch_message(out_file, stop_seq_striped)
