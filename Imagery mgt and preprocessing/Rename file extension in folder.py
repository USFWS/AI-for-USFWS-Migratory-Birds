import glob, os

# Input dir where file extensions need to be changed
os.chdir('F:/AMAPPS_CLASSIFY/silly')

for filename in glob.glob('*.JPG'):
    print(filename)
    pre, ext = os.path.splitext(filename)
    os.rename(filename, pre + '.jpg') # enter the new filename extension