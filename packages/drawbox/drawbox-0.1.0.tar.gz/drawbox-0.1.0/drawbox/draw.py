#!/usr/bin/env python
import sys
import getopt

def usage():
    sys.stderr.write('''Print ascii stack box.
-p (--padding): number of padding space around content

For example:

stdin:

hello
world

output:
+---------+
|  hello  |
|  world  |
+---------+

stdin:

hello
------
line1
line2
line3
---
line4
line5

output:
+----------+
|  hello   |
+----------+
|  line1   |
|  line2   |
|  line3   |
+----------+
|  line4   |
|  line5   |
+----------+''')

def print_text(text):
    sys.stdout.write(text)

def draw(texts, padding = 2):
    max_length = len(max(texts, key=lambda x: len(x)))
    # draw first line
    print_text('+' + '-' * (padding * 2 + max_length) + '+\n')
    for text in texts:
        if len(set(text)) == 1 and text[0] == '-':
            print_text('+' + '-' * (padding * 2 + max_length) + '+\n')
        else:
            print_text('|' + ' ' * padding + text +
                  ' ' * padding +
                  ' ' * (max_length - len(text)) + '|\n')
    # draw bottom
    print_text('+' + '-' * (padding * 2 + max_length) + '+\n')
 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:", ["help", "padding="])
    except getopt.GetoptError as err:
        usage()
        sys.exit(2)
    padding = 2 
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-p", "--padding"):
            padding = a
        else:
            assert False, "unhandled option"
    input_str = sys.stdin.read()
    draw([line for line in input_str.split('\n') 
                   if len(line.strip()) > 0], int(padding))
   
if __name__ == '__main__':
    main()
