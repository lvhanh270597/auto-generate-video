#!/usr/bin/python3
import sys
text = open(sys.argv[1]).read()
start = text.index('[SAR')
end = text.index('DAR', start)
text = text[start + 4 : end].strip()
print(text)