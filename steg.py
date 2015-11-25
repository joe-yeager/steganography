from PIL import Image
import binascii
import numpy
import sys

messageBinary = []
stopSeq = ["00101111","00101111","00101111"]
stopSeqBroken = ["00","10","11","11","00","10","11","11","00","10","11","11"]

def getUserImputAsBinary():
  userInput = raw_input("What's your message?: ")
  for i in range(0,len(userInput)):
    char = userInput[i]
    result = bin(ord(char))[2:].zfill(8)
    messageBinary.append(result)

def transformInput():
  for i in stopSeq:
    messageBinary.append(i)
  tempBuf = []
  for i in range(0, len(messageBinary)):
    for j in range(0, 4):
      tempBuf.append(messageBinary[i][j*2:(j*2)+2])
  return tempBuf

def addMessageToImage():
  image = Image.open("test.jpeg")
  (width, height) = image.size
  imgArry = numpy.array(image)
  if (len(messageBinary) * 4 ) < imgArry.size:
    row = 0
    while len(messageBinary) > 0:
      for i in range (0, width):
        binary = bin(imgArry[row][i][0])[2:].zfill(8)
        if len(messageBinary) == 0:
          break
        blah = binary[:6] + messageBinary.pop(0)
        imgArry[row][i][0] = int(blah,2)
        if row > height:
          break
      row += 1
    
    result = Image.fromarray(imgArry)
    result.save('out.bmp')

def fetchMessageFromImage():
  messageBinary = []
  image = Image.open("out.bmp")
  (width, height) = image.size
  imgArry = numpy.array(image)
  row = 0
  doneFetching = False
  decodeArray = []
  decodedMessage = ""
  while not doneFetching:
    for i in range (0, width):
      messageBinary.append(bin(imgArry[row][i][0])[-2:])
      if messageBinary[-12:] == stopSeqBroken:
        doneFetching = True
        break
      if row > height:
        break
    row += 1
  while len(messageBinary) > 0:
    if len(messageBinary) >= 4:
        tempStr = ""
        for i in range(0,4):
          tempStr += messageBinary.pop(0)
        decodedMessage += chr(int(tempStr,2))
  print "message:", decodedMessage[:-len(stopSeq)]

if len(sys.argv) == 1:
  print "please provide an argument:\n\tencode: to encode a message in test.jpeg\n\tdecode: decode the message in out.bmp"
elif "encode" in sys.argv:
  getUserImputAsBinary()
  messageBinary = transformInput()
  addMessageToImage()
elif "decode" in sys.argv:
  fetchMessageFromImage()




