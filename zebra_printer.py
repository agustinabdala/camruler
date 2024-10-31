import os
from PIL import Image
import zpl
from zebra import Zebra

prompt_print = input("imprimir? (s/n)")

l = zpl.Label(74,74)

height = 0
l.origin(5,3)
l.write_text("ALEX RONCO", char_height=10, char_width=8, line_width=55, justification='C')
l.endorigin()

height += 12
l.origin(5,height)
l.write_text("ZZZZZZ6666", char_height=8, char_width=8, line_width=55, justification='C')
l.endorigin()


height += 10
l.origin(5, height)
l.barcode('C', '07000002198666123456789AB', height=150, check_digit='Y')
l.endorigin()

#CODIGO QR
# l.origin(32, height)
# l.barcode('Q', 'https://github.com/cod3monk/zpl/', magnification=5)
# l.endorigin()

height += 13
image_width = 5
l.origin((l.width-image_width)/2, height)
image_height = l.write_graphic(
    Image.open(os.path.join(os.path.dirname(zpl.__file__), 'trollface-large.png')),
    image_width)
l.endorigin()


height += 20
l.origin(5, height)
l.write_text(' FAdeA ', char_height=10, char_width=4, line_width=55,
             justification='C')
l.endorigin()

label = l.dumpZPL()
l.preview()

if prompt_print == "s":
    z = Zebra()
    Q = z.getqueues()
    z.setqueue(Q[0])
    z.setup(direct_thermal=False)
    z.output(label)
    
else: 
    pass