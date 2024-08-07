story = ''
while True:
    line = input('>>>')
    if not line:
        print("the end")
        break
    story+=line+'\n'
print(f'Your story\n{story}')  