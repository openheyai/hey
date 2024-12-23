# hey

A natural command line interface for your computer.

`hey make the screen darker`
`hey kill that process`
`hey what's using all my memory`

No flags. No options. No manual pages. Just ask for what you want by chatting (with the keyboard or via audio).

`hey` understands context, remembers your preferences, and handles system operations naturally.

Think of it as the universal interface you'd design if you were starting from scratch today, with modern language models and a focus on human-first interaction.

## Status

Early alpha. Core functionality includes process management, system operations, and basic file handling. Expect breaking changes.

```$ hey
< hi! it looks like it's the first time we've met. i'm hey, your general purpose assistant. would you like to see my capabilities? feel free to just ask me to assist you with something immediately.
>
```

```$ hey
* listening on audio device 0, transcription via whisper
< hi again! we didn't get a chance to speak last time - did you want to hear my capabilities?
> 


## core launch capabilities

### system operations

"hey make the screen darker"
"hey mute everything"
"hey show me what's using all my memory"
"hey zip these files"

### development tools

"hey what's using port 3000"

```$ hey kill that process
< the process you just started, or the one that's chewing through 90% more battery than the others?
> the python process 
! hey requested permission to initiate a long running task, send a SIGQUIT signal to a running process (1345) and to get information about the current status of a process. you can allow it, deny it, or ask for more information.
> more info, please
! hey will try sending a SIGQUIT signal to the process, and intends to check the status of the process for up to one minute after to confirm
it's exited. if it's still running, hey will recommend further options that may require other permissions. does that give you enough information?
> permission approved
! hey initiated exponential backoff task to check the exit status of the process for up to 1 minute
! hey sent a SIGQUIT signal to the process
! hey checked the status of process (1345)
> the process didn't quit immediately, but we'll give it a minute to finish.
! hey checked the status of process (1345)
> 
```

"hey show me the last error in the logs"
"hey start the dev server"

### basic file operations

"hey find that file I was working on yesterday"
"hey move these images to my backup folder"
"hey what's taking up so much space"

### quick answers

"hey what time is it in Tokyo"
"hey what's 15% of 847"
"hey remind me how to merge in git"



![hey](https://github.com/user-attachments/assets/45cc2c3f-8ff5-48ee-8acd-3eb2838ea499)

