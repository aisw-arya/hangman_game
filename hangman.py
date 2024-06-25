def get_word():     
    import random
    words_list= open('words.txt','r') 
    word=random.choice(words_list.readlines()).replace('\n','') 
    return(word)

def start(): 
    print('___Welcome__')
    print("""Rules for this game:
            1.Guess a word.
            2.You're allowed to guess using any letter of the alphabet.
            3.You have a total of 7 chances.
            4.If you fail to guess correctly, the hangman will be gradually drawn.""")
    print("Let's start the game.")

    result()  


def image(chance):   #Function to display pictures.
    if chance ==  6:
        print("""|_______\n|  |\n|\n|\n|\n|\n|_""")
    elif chance == 5:
        print("""|_______\n|  |\n|  0\n|\n|\n|\n|""")
    elif chance == 4:
        print("""|_______\n|  |\n|  0\n| / \n|\n|\n|""")
    elif chance == 3:
        print("""|_______\n|  |\n|  0\n| / \\ \n|\n|\n|""")
    elif chance == 2:
        print("""|_______\n|  |\n|  0\n| /|\\ \n|\n|\n|""")
    elif chance == 1:
        print("""|_______\n|  |\n|  0\n| /|\\ \n| /\n|\n|""")
    elif chance == 0:                                                                                                                                                                                                                                                                       
        print("""|_______\n|  |\n|  0\n| /|\\ \n| / \\\n|\n|""")


def masking_word(word):    
          
    masked_word = ""
    for letter in range(0,len(word)):       
        masked_word = masked_word + '-' 
    print(masked_word,len(masked_word), 'Letter word')
    return masked_word 


def previous_choice(guessed_letter,guessed_letter_list):
    if guessed_letter not in guessed_letter_list: 
        guessed_letter_list.append(guessed_letter) 
        
        print('Your previous choices :-',guessed_letter_list)
    else:
        print('You made this choice earlier.')



def unmasking_word(guessed_letter,word,masked_word):
    new_masked_word = list(masked_word)
    for i in range(len(word)):
        if word[i] == guessed_letter:
            new_masked_word[i] = guessed_letter
    return ''.join(new_masked_word)




def validation(guessed_letter):
    if not guessed_letter.isalpha() or len(guessed_letter) != 1:
        print("Please enter a single alphabetic character.")
        return True


def chance_left(guessed_letter,guessed_letter_list,word,chance):
    if guessed_letter not in word and guessed_letter not in guessed_letter_list:
        chance-=1
        image(chance)
        print("chances left",chance)
    if chance == 0: 
        print("You've exhausted your chances,You were eliminated from the game .The word is-",word)
        # exit()
    return chance

def result():
    word = get_word() 
    masked_word=masking_word(word)
    guessed_letter_list=[] 
    chance=7 
    while(chance>0):            
        guessed_letter = input('enter a letter:').lower() 
        if not validation(guessed_letter):
            chance = chance_left(guessed_letter,guessed_letter_list,word,chance)
            previous_choice(guessed_letter,guessed_letter_list)
            if guessed_letter in word:
                masked_word=unmasking_word(guessed_letter,word,masked_word)
        if masked_word == word :    
            print("You've guessed correctly: 'Congratulations on completing the game!'")
            exit()
        print(masked_word)
       

       

if __name__ == "__main__":
    start()




