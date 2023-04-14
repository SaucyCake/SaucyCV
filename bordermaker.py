import sys
import PySimpleGUI as sg
import os.path
sys.path.append('C:/Users/Saucer/AppData/Local/Programs/Python/Python311/Lib/site-packages')
import cv2

recently_modified = []

def startGUI():
    left_col = [[sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()],
                [sg.Listbox(values=[], enable_events=True, size=(40, 20), key='-FILE LIST-')]]

    size = [i for i in range(0, 100)]
    action_col = [[sg.Button('About'), sg.Button('Help')],
                  [sg.HorizontalSeparator()],
                  [sg.Text('Border Size'), sg.Spin(size, initial_value=5, readonly=True,  size=5, enable_events=True, key='Bsize'), sg.Text('%')],
                  [sg.Text('Border Color'),
                   sg.In("", visible=False, enable_events=True, key='set_line_color'),
                   sg.ColorChooserButton("color", size=(10, 1), target='set_line_color',
                                         button_color=('#ffffff', '#ffffff'),
                                         border_width=1, key='set_line_color_chooser')],
                  [sg.Button('Square', key='Square', disabled=True),
                   sg.Button('Square folder', key='Square_folder', disabled=True)],
                  [sg.Button('Portrait', key='Portrait', disabled=True),
                   sg.Button('Portrait folder', key='Portrait_folder', disabled=True)],
                  [sg.Button('Landscape', key='Landscape', disabled=True),
                   sg.Button('Landscape folder', key='Landscape_folder', disabled=True)],
                  [sg.Button('Auto', key='Auto', disabled=True)]]

    recent_col = [[sg.Text('Destination'), sg.In(size=(25, 1), enable_events=True, key='-DESTIN-'), sg.FolderBrowse()],
                  [sg.Listbox(values=[], enable_events=True, size=(40, 20), key='-MODIFY-')]]

    images_col = [[sg.Text('You choose from the list:')],
                  [sg.Text(size=(40, 1), key='-TOUT-')],
                  [sg.Image(key='-IMAGE-')]]

    layout = [
        [sg.Column(left_col, element_justification='left'), sg.VSeperator(),
         sg.Column(action_col, element_justification='center'), sg.VSeperator(),
         sg.Column(recent_col, element_justification='center'),
         ]]

    window = sg.Window('Border Maker', layout, resizable=True)
    flag = {'folder': False, 'destination': False, 'file': False}
    hexcode = '#ffffff'
    Bsize = 5

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == '-FOLDER-':  # Folder name was filled in, make a list of files in the folder
                folder = values['-FOLDER-']
                try:
                    file_list = os.listdir(folder)  # get list of files in folder
                except:
                    file_list = []
                fnames = [f for f in file_list if os.path.isfile(
                    os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                window['-FILE LIST-'].update(fnames)
                flag['folder'] = True
            if event == '-DESTIN-':  # Folder name was filled in, make a list of files in the folder
                destcheck = 1
                destination = values['-DESTIN-']
                flag['destination'] = True
            if event == 'set_line_color':
                window['set_line_color_chooser'].Update(button_color=(values[event], values[event]))
                hexcode = values[event]
            if event == 'Bsize':
                Bsize = values['Bsize']

            elif event == '-FILE LIST-':  # A file was chosen from the listbox
                file = values['-FILE LIST-'][0]
                filecheck = 1
                try:
                    filename = os.path.join(folder, file)
                    #window['-TOUT-'].update(filename)
                    flag['file'] = True
                except Exception as E:
                    print(f'** Error {E} **')
                    pass  # something weird happened making the full filename

            if flag['folder'] and flag['destination']:
                window['Square_folder'].update(disabled=False)
                window['Portrait_folder'].update(disabled=False)
                window['Landscape_folder'].update(disabled=False)
                window['Auto'].update(disabled=False)
                if flag['file']:
                    window['Square'].update(disabled=False)
                    window['Portrait'].update(disabled=False)
                    window['Landscape'].update(disabled=False)

            if event == 'About':
                About()
            if event == 'Help':
                Help()
            if event == 'Auto':
                auto(folder, destination, hexcode, Bsize)
                rm = [f for f in recently_modified if f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                window['-MODIFY-'].update(rm)
            if event == 'Square':
                make_square(folder, file, destination, hexcode, Bsize)
                rm = [f for f in recently_modified if f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                window['-MODIFY-'].update(rm)
            if event == 'Square_folder':
                squarefolder(folder, destination, hexcode, Bsize)
                rm = [f for f in recently_modified if f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                window['-MODIFY-'].update(rm)
            if event == 'Portrait':
                make_portrait(folder, file, destination, hexcode, Bsize)
                rm = [f for f in recently_modified if f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                window['-MODIFY-'].update(rm)
            if event == 'Portrait_folder':
                portraitfolder(folder, destination, hexcode, Bsize)
                rm = [f for f in recently_modified if f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                window['-MODIFY-'].update(rm)
            if event == 'Landscape':
                make_landscape(folder, file, destination, hexcode, Bsize)
                rm = [f for f in recently_modified if f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                window['-MODIFY-'].update(rm)
            if event == 'Landscape_folder':
                landscapefolder(folder, destination, hexcode, Bsize)
                rm = [f for f in recently_modified if f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                window['-MODIFY-'].update(rm)

        window.close()
    except Exception as e:
        print(e)
        # sg.popup_error_with_traceback(f'An error happened.  Here is the info:', e)

def About():
    text = [[sg.Text('Just made this to post on instagram\n'
                     'a simple program to add borders without cropping or decreasing image quality\n'
                     '(limitations of code decreases dpi, so use for online only!!!)\n'
                     'also been interested in computer vision and learning python\n'
                     'so will be adding more, let me know if you have interesting ideas or complaints')],
            [sg.VerticalSeparator()],
            [sg.Text('Contact me, about anything\n'
                     'Discord: Saucy#1112\n'
                     'Instagram: Saucy.archive')],

            ]
    aboutwin = sg.Window('About', text, resizable=True)
    while True:
        event, values = aboutwin.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    aboutwin.close()

def Help():
    text = [[sg.Text('How to use:')],
            [sg.Text('First select a folder with your photos.\n'
                     'Select destination to put the modified photos to. \n'
                     'Then choose an action to take\n'
                     'Square          1:1 aspect ratio\n'
                     'Portrait          4:5 aspect ratio\n'
                     'Landscape     16:9 aspect ratio\n'
                     'Auto the previous 2 based on dimensions\n')],
            [sg.VerticalSeparator()],
            [sg.Text('Additional options:\n'
                     'Border size: changes border of the shorter side \n'
                     'Border Color: changes color of the border\n'
                     '(NOTE!!! the area between magenta and cyan dont work ')],

            ]
    helpwin = sg.Window('About', text, resizable=True)
    while True:
        event, values = helpwin.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    helpwin.close()

def hex_to_rgb(hexcode):
    h = hexcode.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def color_no_crash():
    sg.askcolor(parent=window.TKroot, color=color)[-1]

def squarefolder(folder, destination, hexcode, Bsize):
    for images in os.listdir(folder):
        if images.endswith(".jpg") or images.endswith(".JPG") or images.endswith(".png"):
            make_square(folder, images, destination, hexcode, Bsize)


def make_square(folder, images, destination, hexcode, Bsize):
    img = cv2.imread(folder + "\\" + images, cv2.IMREAD_UNCHANGED)
    wid = img.shape[1]
    hgt = img.shape[0]
    hrgb = hex_to_rgb(hexcode)
    #print(hrgb)
    if wid > hgt:
        nWid = ((wid * (100 + Bsize))/100) - wid
        nHgt = (wid + nWid) - hgt
        bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                  cv2.BORDER_CONSTANT, value=hrgb)

    if wid < hgt:
        nHgt = (hgt * (100 + Bsize))/100 - hgt
        nWid = (hgt + nHgt) - wid
        bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                  cv2.BORDER_CONSTANT, value=hrgb)

    elif wid == hgt:
        nWid = (wid * (100 + Bsize))/100 - wid
        nHgt = (hgt * (100 + Bsize))/100 - hgt
        bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                  cv2.BORDER_CONSTANT, value=hrgb)

    filename = destination + "/" + images.split(".")[0] + "_square.jpg"
    cv2.imwrite(filename, bimg)
    recently_modified.append(filename.split(destination+"/")[1])
    os.chdir(folder)


def portraitfolder(folder, destination, hexcode, Bsize):
    for images in os.listdir(folder):
        if images.endswith(".jpg") or images.endswith(".JPG") or images.endswith(".png"):
            make_portrait(folder, images, destination, hexcode, Bsize)


def make_portrait(folder, images, destination, hexcode, Bsize):
    img = cv2.imread(folder + "\\" + images, cv2.IMREAD_UNCHANGED)
    wid = img.shape[1]
    hgt = img.shape[0]
    hrgb = hex_to_rgb(hexcode)
    if hgt > wid:
        nHgt = ((hgt * (100 + Bsize))/100) - hgt
        nWid = (((nHgt + hgt) / 5) * 4) - wid
        bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                  cv2.BORDER_CONSTANT, value=hrgb)

    if hgt < wid:
        nWid = ((wid * (100 + Bsize))/100) - wid
        nHgt = (((nWid + wid) / 4) * 5) - hgt
        bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                  cv2.BORDER_CONSTANT, value=hrgb)

    elif wid == hgt:
        nWid = ((wid * (100 + Bsize))/100) - wid
        nHgt = ((hgt * (100 + Bsize))/100) - hgt
        bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                  cv2.BORDER_CONSTANT, value=hrgb)

    filename = destination + "/" + images.split(".")[0] + "_portrait.jpg"
    cv2.imwrite(filename, bimg)
    recently_modified.append(filename.split(destination+"/")[1])
    os.chdir(folder)


def landscapefolder(folder, destination, hexcode, Bsize):
    for images in os.listdir(folder):
        if images.endswith(".jpg") or images.endswith(".JPG") or images.endswith(".png"):
            make_landscape(folder, images, destination, hexcode, Bsize)


def make_landscape(folder, images, destination, hexcode, Bsize):
    img = cv2.imread(folder + "\\" + images, cv2.IMREAD_UNCHANGED)
    wid = img.shape[1]
    hgt = img.shape[0]
    hrgb = hex_to_rgb(hexcode)
    if wid == hgt:
        nWid = ((wid * (100 + Bsize))/100) - wid
        nHgt = ((hgt * (100 + Bsize))/100) - hgt
        bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                  cv2.BORDER_CONSTANT, value=hrgb)
    else:
        nHgt = ((hgt * (100 + Bsize))/100) - hgt
        nWid = ((hgt + nHgt) * (16/9)) - wid
        bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                  cv2.BORDER_CONSTANT, value=hrgb)

    filename = destination + "/" + images.split(".")[0] + "_landscape.jpg"
    cv2.imwrite(filename, bimg)
    recently_modified.append(filename.split(destination+"/")[1])
    #print(filename + " done")
    os.chdir(folder)

def auto(folder, destination, hexcode, Bsize):
    for images in os.listdir(folder):
        if images.endswith(".jpg") or images.endswith(".JPG") or images.endswith(".png"):
            img = cv2.imread(folder + "\\" + images, cv2.IMREAD_UNCHANGED)
            wid = img.shape[1]
            hgt = img.shape[0]
            hrgb = hex_to_rgb(hexcode)

            if wid > hgt:
                # ratio = 1.91/1
                nHgt = ((hgt * (100 + Bsize)) / 100) - hgt
                nWid = ((hgt + nHgt) * (16/9)) - wid
                bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                          cv2.BORDER_CONSTANT, value=hrgb)
                filename = destination + "/" + images.split(".")[0] + "_landscape.jpg"

            if wid < hgt:
                # ratio = 4/5
                nHgt = ((hgt * (100 + Bsize)) / 100) - hgt
                nWid = (((nHgt + hgt) / 5) * 4) - wid
                bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                          cv2.BORDER_CONSTANT, value=hrgb)
                filename = destination + "/" + images.split(".")[0] + "_portrait.jpg"

            elif wid == hgt:
                nWid = ((wid * (100 + Bsize)) / 100) - wid
                nHgt = ((hgt * (100 + Bsize)) / 100) - hgt
                bimg = cv2.copyMakeBorder(img, round(nHgt / 2), round(nHgt / 2), round(nWid / 2), round(nWid / 2),
                                          cv2.BORDER_CONSTANT, value=hrgb)
                filename = destination + "/" + images.split(".")[0] + "_square.jpg"

            cv2.imwrite(filename, bimg)
            recently_modified.append(filename.split(destination + "/")[1])
            os.chdir(folder)


if __name__ == "__main__":
    startGUI()
