import os


def main():
    i = 0

    folder = "C:/Users/hsamak/Documents/logos"
    for filename in os.listdir(folder):
        src = filename

        filename = filename[:filename.index("-logo")]
        name_array = filename.split('-')
        dst = ''
        for name_part in name_array:
            dst =  dst + ' ' + name_part.capitalize()
        dst = dst.strip()+'.png'
        # rename() function will
        # rename all the files
        print(src)
        print(dst)
        os.rename(os.path.join(folder, src), os.path.join(folder, dst))



# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()