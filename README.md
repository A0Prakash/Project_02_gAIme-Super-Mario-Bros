# Project_02_gAIme-Super-Mario-Bros
AI to play Super Mario Bros and implementation of that AI in pygame.
## Introduction
I have been playing the classic super mario bros for around 10 years on the classic console. When I discovered that recreations in pygame existed, I really wanted to make an AI that could beat my aunt(the goat at super mario bros), because I am really horrible at super mario bros.

## Gym
### Explanation
OpenAI created something called gym for enviroment simulation of atari style games. Someone has made one of these enviroments for super mario bros: gym_super_mario_bros(credit to Alex letting me know that gym exists and sending me this python library)
### Implementation
Given these enviroments, I was able to create a Neural Network that learned based on the state and reward system. Basically, given the agent(Mario or the AI) is given a state(the enviroment around him) and makes a decision on what to do based on the state. However, when it doesn't know what to do or can't make decisions, it has to learn. In order to learn, we use reward. Mario does random things and when it does something good--in our case it moves further right without dying in a timely manner-- it is given a more positive reward. Based on these rewards, our Agent is able to discern what is good and what is not good. I created two classes, AgentNN and Agent. The AgentNN class was just a neural network class, but the Agent class was the actual model that was learning. I had two AgentNNs, a main and a target, and I took an epsilon greedy approach in training the main network, which is what actually made the decisions. Basically, the epsilon greedy approach encourages random movements while mario is learning to see if mario can come up with a better reward. As epsilon decays, Mario stops trying new things. I saved the models as pytorch models.

## PyGame
### Explanation
For this project, I needed to get my AI to work in PyGame. In order to do this, I had to recreate the gym enviroment in the pygame game that I got from this link: https://github.com/Winter091/MarioPygame. In the Core file, I located the main loop, which looped each frame of the game. In this loop, I was able to get an image from pygame.
### Gym Wrapper Implementation
Gym uses wrappers to make the data that the enviroment feeds into the model possible to go into the model. However, I needed to do this with the image I got from pygame. The first two wrappers were resize and grayscale. Basically resizing the image and turning the shape into (84, 84, 3), and then after grayscaling the image to make the shape (84,84). After this, I needed to implement the framestack and skipframe wrapper. It was difficult to understand how these worked in tandem, so it took a while to find this piece of literature: https://danieltakeshi.github.io/2016/11/25/frame-skipping-and-preprocessing-for-deep-q-networks-on-atari-2600-games/. This explained the theory behind framestack and skipframe. Basically, once every certain amount of frames, the model adds that frame to a queue and once the queue is full(threshold), it creates an array of shape (threshold,84,84). In our case (4,84,84), and then after this, it will remove the first element in the queue and add another element to the end of the queue to stack it. 
### Final Model Running in PyGame
After implementing the wrappers, I was able to import the Agent into the pygame game, and allow it to make decisions without epsilon(only making decisions, not learning). Based on the output(int from 0 to 4), I added an input function to allow outputs to control the mario in the pygame.

## Results
### Limitation
I had a few limitations, the main one being processing power. It took around 2 days to get through 2000 iterations. Most of the models I could see online got 50000 iterations with a 3080(GPU) in two days. I didn't use my PC to train this but my mac, and therefore I was severely limited by time and processing power.
### Performance
In the end, Mario doesn't perform very well. I hope to improve my model in the future. My primary mistake was setting the epsilon decay too high, meaning that mario tries a bunch of random actions and never really gets rewarded for repeating actions. In the future, if I had more time ot train Mario and parameter tune, I would be able to get a better performing Mario.

## Sources
*https://www.youtube.com/watch?v=_gmQZToTMac
*https://github.com/Sourish07/Super-Mario-Bros-RL
*https://github.com/Winter091/MarioPygame
*https://danieltakeshi.github.io/2016/11/25/frame-skipping-and-preprocessing-for-deep-q-networks-on-atari-2600-games/
