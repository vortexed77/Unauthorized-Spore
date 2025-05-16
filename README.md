

# Unauthorized-Spore  
Some old project I created for fun, with very corny 'responses'.

> [!WARNING]  
> This project may contain bugs. I tested most of the stuff out and haven't found any bugs.  
> If you find an issue in the program, please let me know.

---

## Commands

**Observe**  
**Usage:** `observe /core/alpha/root_1/sp01`  
Returns the status of that spore.

**Init_root**  
**Usage:** `init_root root_4`  
Creates a new root. Slowly generates new spores onto that root (takes a while).

**Pop_spore**  
**Usage:** `pop_spore /core/alpha/root_1/sp01`  
Pops the specified spore. Will fail if the spore is already ruptured.

**Terminate**  
**Usage:** `terminate /core/alpha/root_1`  
Terminates a root. Might fail, might succeed.

**Halt_all**  
**Usage:** `halt_all`  
Attempts to shut the core down. Very **unlikely** to succeed.

**Reveal**  
**Usage:** `reveal /core/alpha/root_1/sp01` or `reveal /core/alpha/root_1`  
Uncovers any data for that root/spore logged by another person.

**Echo**  
**Usage:** `echo "Who are you?"`  
Sends a message into the core. You might get a response back...  
**WARNING:** The command only works if your message is in quotation marks (e.g., `"hello"`).

**Seed**  
**Usage:** `seed /core/alpha/root_1`  
Plants a new latent spore inside the specified root.

**Silence**  
**Usage:** `silence`  
Disables output.

---

## About

I created this project to practice my Python skills. I was into the horror scene and wanted to make something creepy.  
The responses are VERY corny — I'm not the best at horror, honestly.

### What the program is based on:  
Multiple roots exist inside a core. Each root contains spores with different statuses (e.g., *watching*, *latent*, *ruptured*, etc).  
It's a terminal meant for controlling the core. Although for some reason, **You** have access to it now.

---

