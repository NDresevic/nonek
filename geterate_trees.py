import os
path = '.\examples'

print('PROCESSING...')
for dir_name in os.listdir(path):

    dot_pos = dir_name.find('.')
    if dot_pos < 0 :
        continue

    ext = dir_name[dot_pos+1:]
    dir_name = dir_name[:dot_pos]

    dir_path = os.path.join(path, dir_name)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    dir_name = os.path.join(dir_path, dir_name)

    input_filename = '{}.{}'.format(dir_path, ext)
    dot_filename = '{}.dot'.format(dir_name)
    png_filename = '{}.png'.format(dir_name)

    os.system('python getastdot.py {} > {}'.format(
        input_filename,
        dot_filename
    ))


print('DONE')

