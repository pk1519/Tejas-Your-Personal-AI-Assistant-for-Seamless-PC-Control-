def get_user_input_method():
    print("Please choose your input method:")
    print("1. Voice Input")
    print("2. Text Input")

    choice = input("Enter 1 for Voice, 2 for Text: ")

    if choice == '1':
        print("Voice input selected.")
        return 'voice'
    else:
        print("Text input selected.")
        return 'text'


