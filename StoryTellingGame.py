from openai import OpenAI
import re

client = OpenAI(
    api_key=open(".API_KEY", "r").read() #Change .API_KEY to file which contains your OPENAI_API_KEY
)

# Prompting User to enter the world in which the model will play a story from
game_type = input('\nIn which fictional world would you like the story to happen?\n' \
                  'You can be as descriptive as you want and the fictional world ' \
                  'can be from an existing story or one that you describe the environment.\n\n')

# Will be used to store data of the game to refeed into the model and initialization
story = [
        {"role": "system", "content": 'You are the narrator for a story telling game where '\
         'anything can happen. The game should be descriptive, eventful yet concise and be played '\
         f'in the world of {game_type}. Describe the starting point and ask the user what they want to do. '\
         'The storyline unravels as the player advances until he dies or reaches the final plot. '\
         'If the player wants to end the game or reaches plot, finish message with THE END '\
         'Rule to follow: Please Keep the narrations concice, i.e no more than 150 words.'
         },
        {"role": "user", "content": "Start the game"}
        ]

# Getting chat model narration output
def get_completion_from_messages(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    story.append({"role": "assistant", "content": response.choices[0].message.content.strip("\n").strip()})
    return response.choices[0].message.content
    
# Getting user's action
def get_user_choice():
    choice = input("\n")
    story.append({"role": "user", "content": choice})
    return choice

# Game loop feeding back into the story logs
while True:
    narration = get_completion_from_messages(story)
    print(f"\n\t{narration}")
    if re.search('THE END', narration):
        break
    if re.search("q[uit]{0,3}", get_user_choice()):
        break

print("\nThanks for playing the game!\n")