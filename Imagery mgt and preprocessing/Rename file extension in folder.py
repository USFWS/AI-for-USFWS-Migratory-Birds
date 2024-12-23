import glob,os

# Input dir where file extensions need to be changed
os.chdir('E:/Flights/20241219_150200_rawonly/Overviews/0')
source_dir = 'E:/Flights/20241219_150200_rawonly/Overviews/0/'
export_dir = 'E:/Flights/20241219_150200_rawonly/Overviews/new2/'

for filename in glob.glob('*.JPG'):
    print(filename)
    pre, ext = os.path.splitext(filename)
    rename1 = pre + '.jpg'
    print ("Rename: ", rename1)
    os.rename(os.path.join(source_dir, filename),
              os.path.join(export_dir, rename1)) # enter the new filename extension
