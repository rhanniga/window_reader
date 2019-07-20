from sys import argv
import datetime
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

current_date = datetime.datetime.today()


#cOmPuTErS aRE sOoOO SmARt
def remove_commas(str):
    new_str = ''
    for char in str:
        if char == ",":
            new_str += "."
        else:
            new_str += char
    return new_str
            
def write_to_file(log_file_name, values):
    log_file = open(log_file_name, "a+")

    log_file.write("\n")

    log_file.write(str(current_date.year) + "-" + str(current_date.month) + "-" + str(current_date.day))
    log_file.write("    ")
    if current_date.hour > 9:
        log_file.write(str(current_date.hour) + str(current_date.minute))
    else:
        log_file.write("0" + str(current_date.hour) + str(current_date.minute))
    log_file.write("    ")

    for index, value in enumerate(values):
        if index != len(values) - 1:
            log_file.write(str(value) + "   ")
        else:
            log_file.write(str(value))
    log_file.close()

#list to store the actual values written to the file
values = []

#all of these measurements are in pixels
box_height = 14
displacement = 12.5
box_width = 29

wincc = Image.open("wincc.png")

#reading iMon
imon_left = 420
imon_top = 718
for row in range(11):
    box_dim = [imon_left, imon_top + (displacement*row), imon_left + box_width, imon_top + (displacement*row) + box_height]
    box = wincc.crop(box_dim)
    value = remove_commas(pytesseract.image_to_string(box))
    if row == 10:
        vbb = value
    else:
        values.append(value)
values.insert(0, vbb)

#reading external
box_dim = [629, 94, 663, 108]
box = wincc.crop(box_dim)
box.save("external.png")
value = remove_commas(pytesseract.image_to_string(box))
values.append(value)

#reading other temps
temp_left = 298
temp_top = 104
box_width += 7
box_height -= 0.03
for row in range(6):
    box_dim = [temp_left, temp_top + (displacement*row), temp_left + box_width, temp_top + (displacement*row) + box_height]
    box = wincc.crop(box_dim)
    box.save(f"box_{row}.png")
    value = remove_commas(pytesseract.image_to_string(box))
    values.append(value)

write_to_file(argv[1], values)