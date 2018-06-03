import img2pdf
import argparse
import os

header = """
                              ,      \    /      ,
                             / \     )\__/(     / \\
                            /   \   (_\  /_)   /   \\
    _______________________/_____\___\@  @/___/_____\\____________________
   |                                 |\../|                              |
   |                                  \VV/                               |
   |   _______ _______  ______ _______  _____  _  _  _ _______ __   _    |
   |   |  |  | |_____| |_____/ |       |     | |  |  | |______ | \  |    |
   |   |  |  | |     | |    \_ |_____  |_____| |__|__| |______ |  \_|    |
   |_____________________________________________________________________|
     || ||               |    /\ /     \\\\     \ /\    |
     || ||               |  /   V       ))     V   \  |
     || ||               |/     `      //      '     \|
     || ||               `             V              '
    _||_||________________
   |                      |
   | FlipHTML5 IMG -> PDF |
   |______________________|
   """
print(header)
parser = argparse.ArgumentParser()
parser.add_argument("folderName", help="The folder containing images to be converted into pdf")
parser.add_argument("start", help="Starting image number to be converted", type=int)
parser.add_argument("end", help="Last image number to be converted", type=int)
args = parser.parse_args()
folderName = args.folderName
start = args.start
end = args.end

print("Converting...")
images = []
for num in range(start, end+1):
    filepath = "{0}/{1}.jpg".format(folderName, num)
    with open(filepath, "rb") as image:
        images.append(image.read())

with open("{0}.pdf".format(folderName), "wb") as file:
    file.write(img2pdf.convert(images))

print("\rFinished. Press any key to continue")
input()
