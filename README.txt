
Student name: Michelle Lu	



Purpose:
+ This is the Final Project for the SI 106 course at the University of Michigan (Fall 2017).
+ chatbot.py is a simple python AIML chatbot that can be used to extract basic weather information. 



Abilities:
+ chatbot.py can provide a response to the following prompts:
	- "What's the weather like in {city}?"
	- "Is it going to rain in {city} today?"
	- "Is it going to rain in {city} this week?"
	- "How hot will it get in {city} today?"
	- "How hot will it get in {city} this week?"
	- "How cold will it get in {city} today?"
	- "How cold will it get in {city} this week?"



Instructions:
+ Users should download the entire DarkSkyNet zip file.
+ Users may save this zip file on their Desktop or computer location of their choice.
+ Users should use Terminal (Mac) or Command Prompt (PC) in order to navigate to the specific location where they saved the zip file. 
+ Users should run the file titled "chatbot.py"
+ Amongst the many responses the program can output (to various user inputs), to start out -- users may test out the following interactions and expect to receive the following responses:
	
	User: > hello!
	Chatbot: What can I call you?

	User: > {name} 
	Chatbot: Nice to meet you {name}.
	
	User: > Are you a robot?
	Chatbot: How did you know I am a machine?

+ As for weather information, please refer to the "Abilities" section above to see which prompts a user may input and expect to receive specific weather data. 



Notes to user:
+ Sometimes a "keyboard smash" answer such as "What's the weather like in fjaiowejfoiawejfoiej?" will not return "Is fjaiowejfoiawejfoiej a city?" (even though it should). Instead it will return a "valid" answer such as "Sunny". 
+ This could be due to the API in which case the program is searching for the closest city name that matches the "keyboard smash" input.
+ When asking if it is going to rain in a city for either today or this week, keep in mind that the source code is taking into account precipitation probability -- meaning we are not only factoring in rain, but also other types of precipitation such as snow.



