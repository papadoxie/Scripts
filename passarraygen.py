def main():
    
    infile = open('passwords.txt', 'r')
    outfile = open('pass.txt', 'w+')

    for line in infile:
        outfile.write(f'\"{line.strip()}\",\n')

    infile.close()
    outfile.close()

if __name__ == '__main__':

    main()
