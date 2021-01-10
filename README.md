# Cirrus

![image](https://cdn.discordapp.com/attachments/797517358247313431/797924612045537321/add.png)

As the school year comes closer (or has already started for some people), we were thinking of a way to help students easily track their own assignments through one of the many online social platforms that students may use. We assessed our own needs as students and came up with this bot, Cirrus!

Cirrus has much of the functionality that a student may need. We have commands to add, delete, list, get and clear assignments from our database. When called, Cirrus also displays this information nicely in a visual manner, making it easy to distinguish which command was run.

Remote schooling has become a staple of our curriculum now, whether we like it or not, and projects like these can make it a bit easier to handle. We learned a lot in this project and hope that students have a safe school term/year!  :heart:

Link to the demo video: [Cirrus Demo](https://www.youtube.com/watch?v=J--RJCa_BZw)

[Devpost submission](https://devpost.com/software/cirrusbot)

## Usage
Currently implemented commands:
```
!add     Adds an assignment to the database
!clear   Clears ALL assignments from the list
!delete Delete indicated assignment by ID and assignment name
!echo   Repeats your message
!get      Get indicated assignment by ID and assignment name
!help    Shows the help message
!list      List all assignments added
!ping    Responds to ping for testing purposes
```

## Contributors 

### [Chloe Glave](https://github.com/Cragzu)
* Developed helper function for prettier Discord embeds to make the messages look more user-readable
* Set up the bot and hosted it on Heroku
* Created list command for listing all assignments in the database
* Wrote documentation for the project 

### [Janelle Kwok](https://github.com/Jkcadee)
* Created DynamoDB database and handled DB session in the code and on Heroku
* Implemented add command for adding an assignment to the database
* Built the delete and get commands for deleting and getting a specific assignment in the database
* Added error handling

### [Jugveer Sandher](https://github.com/Jugveer)
* Filmed and edited our demo video
* Helped us test our commands
* Created and handled our Devpost submission

## Credits
This project was created using the discord.py API and AWS's boto3 library.

Thanks to the organizers, mentors and sponsors of this year's nwHacks! You all are awesome and we hope to participate again soon!
