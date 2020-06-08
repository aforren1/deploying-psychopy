import sys
import os
import os.path as op

if getattr(sys, 'frozen', False):
    app_path = sys._MEIPASS
    frozen = True
else:
    app_path = op.dirname(op.abspath(__file__))
    frozen = False

if __name__ == '__main__':
    from psychopy import visual, event, core
    from PIL import Image
    from glob import glob
    from random import randint
    from psychtoolbox import PsychHID, GetSecs
    import numpy as np
    import csv

    GetSecs() # pre-run
    def store_start(dct):
        dct['start_time'] = GetSecs()
    
    win = visual.Window(size=(800, 800), units='height')

    # import images
    img_path = op.join(app_path, 'imgs')

    img_names = glob(op.join(img_path, '*.jpeg'))
    img_names.extend(glob(op.join(img_path, '*.jpg')))
    
    imgs = []
    for img_name in img_names:
        img = Image.open(img_name)
        # rescale to have same height (& fewer pixels)
        max_height = 512
        ratio = max_height/img.height
        img.resize((int(img.width*ratio), max_height))
        ratio2 = img.width/img.height
        img = visual.ImageStim(win, image=img, size=(0.4*ratio2, 0.4))
        basename = op.basename(img_name)
        if basename.startswith('a'):
            awake = True
        else:
            awake = False
        imgs.append({'img': img, 'awake': awake, 'name': basename})
    
    instr_txt = ("In this experiment,\npress the left key (←) when you see a sleeping cat,\n" +
                 "and the right key (→) when you see an awake cat.\n" +
                 "Respond as quickly as possible!\n\nPress any key to start.")
    
    instructions = visual.TextStim(win, instr_txt, height=0.2/5)

    good_txt = visual.TextStim(win, 'GOOD', height=0.1, color='green')
    bad_txt = visual.TextStim(win, 'BAD', height=0.1, color='red')

    # input setup
    key_list = np.zeros(256)
    key_list[36] = 1 # left key
    key_list[38] = 1 # right key
    PsychHID('KbQueueCreate', 0, key_list)

    # trial order
    num_trials = 10
    indices = [randint(0, len(imgs)-1) for i in range(num_trials)]
    block_data = [dict.fromkeys(['awake', 'name', 'start_time', 'rt', 'choice', 'correct']) 
                  for i in range(num_trials)]

    instructions.draw()
    win.flip()
    event.waitKeys()

    core.wait(2)

    PsychHID('KbQueueStart', 0)
    for index, trial_data in zip(indices, block_data):
        imgs[index]['img'].draw()
        PsychHID('KbQueueFlush', 0)
        win.callOnFlip(store_start, trial_data)
        win.flip()
        key_down = False
        while not key_down:
            key_down, first_key_press_times, *others = PsychHID('KbQueueCheck', 0)
        
        # calculate RT, choice
        sq_times = np.squeeze(first_key_press_times)
        idx = np.where(sq_times > 0)[0][0]
        rt = sq_times[idx] - trial_data['start_time']

        # save data
        trial_data['awake'] = imgs[index]['awake']
        trial_data['name'] = imgs[index]['name']
        trial_data['rt'] = float(rt)
        trial_data['choice'] = 'left' if idx == 36 else 'right'
        print(idx, rt, trial_data['awake'])
        if idx == 36 and not trial_data['awake']:
            feedback = good_txt
            correct = True
        elif idx == 38 and trial_data['awake']:
            feedback = good_txt
            correct = True
        else:
            feedback = bad_txt
            correct = False
        
        trial_data['correct'] = correct

        feedback.draw()
        win.flip()
        core.wait(1)

    win.close()

    keys = block_data[0].keys()
    # if we're using the pyinstaller version, save it at the same level as the launcher
    if frozen:
        pth = '..'
    else:
        pth = '.'
    with open(op.join(app_path, pth, 'data.csv'), 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(block_data)
