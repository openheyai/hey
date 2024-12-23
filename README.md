# hey

A natural command line interface for your computer.

## Overview

`hey` is a revolutionary CLI that lets you interact with your computer through natural language. Simply type or speak commands like:

```
hey make the screen darker
hey kill that process
hey what's using all my memory
```

No flags. No options. No manual pages. Just ask for what you want in plain language, either by typing or speaking.

`hey` understands context, remembers your preferences, and handles system operations naturally. Think of it as the universal interface you'd design if you were starting from scratch today, with modern language models and a focus on human-first interaction.

## Status

Early alpha. Core functionality includes process management, system operations, and basic file handling. Expect breaking changes.

## Features

### System Operations
- Adjust screen brightness
- Control audio settings
- Monitor system resources
- Compress files
- And more...

### Development Tools
- Port management
- Process control with interactive confirmation
- Log analysis
- Development server management

Example interaction:
```
$ hey kill that process
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
```

### File Operations
- File search with context ("that file I was working on yesterday")
- Bulk file operations
- Storage analysis and management

### Quick Answers
- Time zone conversions
- Basic calculations
- Development reference (git commands, etc.)

## Getting Started

When you first run `hey`, you'll be greeted with:

```
$ hey
* listening on audio device 0, transcription via whisper
< hi! it looks like it's the first time we've met. i'm hey, your general purpose assistant, how can i help you?
> 
```

you can either speak or type. `hey` can also speak back. 

## Commands

Here are some examples of what you can do with `hey`:

### System Operations
```
hey make the screen darker
hey mute everything
hey show me what's using all my memory
hey zip these files
```

### Development
```
hey what's using port 3000
hey show me the last error in the logs
hey start the dev server
```

### File Management
```
hey find that file I was working on yesterday
hey move these images to my backup folder
hey what's taking up the most space on /?
```

### Quick Information
```
hey what time is 15:32UTC in ET?
hey when's a good time for me to meet with someone in Chennai?
hey what's 15% of 847
hey who was the first person who modified this file, and what commit was it?
hey who made the most contributions to this repo last week?
```

## To Evaluate

Potential future features based on common user queries:

### Productivity & Personal Assistant
```
hey what are the highest rated stories on HN right now?
hey what have I missed on HN since we last checked it?
hey what do I have assigned to me on github right now
hey what's on my calendar for today
hey what's Sarah's birthday
hey let Jeff know I'm running ten minutes late
```
