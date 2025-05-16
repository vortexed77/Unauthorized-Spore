import random
import threading
import time
import sys
import datetime
import math
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtCore import QTimer

# ************* Settings *************

#spore_sprout_chance = 1
terminate_root_chance = 20
halt_all_chance = 1000
structure_data_chance = 10
core_response_chance = 20
spore_core_failure_chance = 50
active_spore_chance = 20

# ************* Settings *************

# Notes:
# S = Spore, R = Root (Outdated)
# Each root has a random amount of spores, Cannot exceed 200 (Memory saving), Minimum is 50

# Lines like this: path = command[len("halt_all") + 1] essentially means everything after "halt_all". It would be the argument.
# Also, The for loop if-statements " if path[i] == 's' and path[i + 1] == 'p' " usually means we are on this character: "/core/alpha/root_1/sp01"
#                                                                                                                                           ^

# Other ones like " if path[i] == 'r' and path[i + 1] == 'o' " means we are on this character: "/core/alpha/root_1/sp02"
#                                                                                                           ^


# Another one that might be a bit confusing to understand is " root_path = path[:-len(spore_name) - 1] "
# It means we are removing the spore's name from the path, Then removing one more character (To remove the slash, Cause the argument provided should look like)
# "/core/alpha/root_1/sp01"
#                    ^ Removing this character

# This is easier to understand if you know about string splicing.

uninitialized_roots = 0

debounces = {
    "echo_debounce": False,
    "kill_root": 0,
    "halt_all": False
}

core_loc = "/core/alpha/"
core_dict = {}

core_responses = {
    "who are you": ("You know.", "You.", "Look in the mirror."),
    "why are you here": ("To watch you.", "To watch your flesh slowly decay."),
    "i hate you": "The mind shows hate towards itself.",
    "die": "I live continuously, Whilst your flesh decays slowly.",
    "hi": ("Hello", "?"),
    "hello": ("Hello", "?")
}

root_terminate_denied_messages = (
    "We see you", "(4)->(2)(933((2)4))"
)

structure_types = {
    "root": ("It's breathing..", "unseen_unforgiven", "Thriving"),
    "spore": ("Growing inner roots", "The inner-roots want air")
}

spore_statuses = [
    "stable", "unstable", "ruptured", "watching", "flickering", "latent"
]

# Functions

# def process_subroot(root_path, spore_name): ill add this back later on, since you cant even observe the spores or pop them, so its pointless
#
#    for j in range(1, random.randint(50, 200)):
#        time.sleep(random.randint(1, 1))
#        print("Updated subroot with a new spore")
#        core_dict[root_path][spore_name]["sub_root"]["spores"].update({f"sp{j:02d}": {"status": random.choice(spore_statuses)}})

def process_root(root_path): # Slowly grow more spores
    global uninitialized_roots
    uninitialized_roots += 1
    for j in range(1, random.randint(50, 200)):
        time.sleep(random.randint(10,60))
        addSpore(j, root_path)
    if not uninitialized_roots == 0: uninitialized_roots =- 1

def addSpore(spore_number, root_path): 
    if root_path in core_dict:
        core_dict[root_path].update({f"sp{spore_number:02d}": {"status": random.choice(spore_statuses)}})
        if random.randint(0, structure_data_chance) == structure_data_chance and not core_dict[root_path][f"sp{spore_number:02d}"]["status"] == "ruptured":
            core_dict[root_path][f"sp{spore_number:02d}"].update({"struct_type": random.choice(structure_types['spore'])})
    else:
        core_dict[root_path] = {f"sp{spore_number:02d}": {"status": random.choice(spore_statuses)}}
        if random.randint(0, structure_data_chance) == structure_data_chance:
            core_dict[root_path].update({"struct_type": random.choice(structure_types['root'])})

def getFormattedTime():
    return datetime.datetime.now().strftime("%H:%M:%S")

def update_value(value, new_value):
    value = new_value

# Etc

for k in range(1, 3):
    root_path = f"{core_loc}root_{k}"

    for j in range(1, random.randint(50, 200)):
        addSpore(j, root_path)

# Main Program

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100,100,500,500)

        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)

        self.terminal_input = QLineEdit()
        self.terminal_input.returnPressed.connect(self.processCommand)

        self.terminal_input_send = QPushButton()
        self.terminal_input_send.clicked.connect(self.processCommand)
        self.InitUI()
    
    def InitUI(self):
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.vLayout = QVBoxLayout()

        self.vLayout.addWidget(self.terminal)
        self.vLayout.addWidget(self.terminal_input)
        self.vLayout.addWidget(self.terminal_input_send)

        self.terminal_input.setPlaceholderText("Input command here..")
        self.terminal_input_send.setText("Send")


        self.setStyleSheet("""
            QTextEdit{
                background-color: black;
                font-size: 15px;
                color: lightgreen     
            }
            QPushButton{
                font-size: 20px;
            }
            QLineEdit{
                background-color: black;
                font-size: 20px;
                color: lightgreen   
            }
        
        """)

        self.mainWidget.setLayout(self.vLayout)

    def send(self, message, wait_time):
        QTimer.singleShot(wait_time*1000, lambda: self.terminal.append(f"{getFormattedTime()} {message}"))

    # Main

    def processCommand(self):
        command = self.terminal_input.text()
        self.terminal_input.clear()
        
        if command.strip():     

            if command.lower() == "silence":
                self.terminal_input.setEnabled(False)
                wait_time = random.randint(10, 20)
                
                self.send(f"[SERVER]> Silence breached", wait_time)
                QTimer.singleShot(wait_time*1000, lambda: self.terminal_input.setEnabled(True))

            elif command.lower().startswith("seed"):
                path = command[len("seed") + 1:].lower()

                if path in core_dict:
                    new_spore_number = 0

                    # Get accurate spore count
                    if "struct_type" in core_dict[path]:
                        new_spore_number = len(core_dict[path]) + 1 - 1
                    else:
                        new_spore_number = len(core_dict[path]) + 1
                    
                    # Plant spore
                    new_spore_name = f"sp{new_spore_number:02d}"

                    addSpore(new_spore_number, path)
                    core_dict[path][new_spore_name]["status"] = spore_statuses[5]
                    self.send(f"[SERVER]> Planted spore '{path}/sp{new_spore_number:02d}'", 3)

                    if random.randint(0, active_spore_chance) == active_spore_chance: # Should spore become active later on?
                        QTimer.singleShot(random.randint(20, 25)*1000, partial(update_value, core_dict[path][new_spore_name]["status"], spore_statuses[0]))
                else:
                    self.send(f"[SERVER]> Invalid root '{path}'", 2)


                    


            elif command.lower().startswith("echo"):
                message = command[len("echo") + 1:]
                
                if not debounces["echo_debounce"]:
                    if message.startswith('"') and message.endswith('"'):
                        debounces["echo_debounce"] = True
                        psy_message = message[1:len(message) - 1]

                        self.send(f"[SERVER]> Message received", 3)
                        QTimer.singleShot(25000, partial(update_value, debounces["echo_debounce"], False))

                        if random.randint(0, core_response_chance) == core_response_chance and psy_message.lower() in core_responses:
                            response = ""
                            if isinstance(core_responses[psy_message.lower()], str):
                                response = core_responses[psy_message.lower()] # if its a string, just use it directly
                            else:
                                response = random.choice(core_responses[psy_message.lower()]) # otherwise grab a random response
                            self.send(f"[SERVER]> Received message from 'CORE': '{response}'", random.randint(20, 30))
                    else:
                        self.send(f"[SERVER]> Message must be in-between quotation marks", 2)
                else:
                    self.send(f"[SERVER]> Failed to send message", 2)

                    
                    


            elif command.lower().startswith("reveal"):
                path = command[len("reveal") + 1:].lower()
                spore_name = None

                for i in range(0, len(path) - 1):
                    if path[i] == "s" and path[i + 1] == "p":
                        spore_name = path[i:]
                        break
                if not spore_name == None: root_path = path[:-len(spore_name) - 1]

                # Root Type
                if path in core_dict and spore_name == None: #example /core/alpha/root_1
                    if "struct_type" in core_dict[path]:
                        struct_type_data = core_dict[path]["struct_type"]
                        self.send(f"[SERVER]> Data recovered for root '{path}': '{struct_type_data}'", 4)
                    else:
                        self.send(f"[SERVER]> Unable to recover data for root '{path}'", 3)
                elif spore_name and core_dict[root_path][spore_name]: #example /core/alpha/root_1/sp01
                        if "struct_type" in core_dict[root_path][spore_name]:
                            struct_type_data = core_dict[root_path][spore_name]["struct_type"]
                            self.send(f"[SERVER]> Data uncovered for spore '{path}': '{struct_type_data}'", 3)
                        else:
                            self.send(f"[SERVER]> Unable to recover data for spore '{path}'", 2)
                else: #invalid argument provided
                    self.send(f"[SERVER]> Unknown path '{path}'", 2)


            elif command.lower() == "halt_all":

                if not debounces["halt_all"]:
                    debounces["halt_all"] = True
                    QTimer.singleShot(random.randint(120000,250000), partial(update_value, debounces["halt_all"], False))
                    if random.randint(0, halt_all_chance) == halt_all_chance:
                        self.send("[SERVER]> Initiating core lockdown", 2)
                        self.terminal_input.setDisabled(True)
                        self.send("[SERVER]> Core has been locked successfully", 25)
                    else:
                        if random.randint(0, 10) == 10:
                            self.send("[SERVER]> You were heard", 2)
                        else:
                            self.send("[SERVER]> Core ignored command", 2)
                else:
                    self.send("[SERVER]> Too many attempts to initiate core lockdown, Try again later", 2)


            elif command.lower().startswith("terminate"):
                path = command[len("terminate") + 1:].lower()
                
                if path in core_dict:
                    root_name = ""

                    for i in range(0, len(path) - 1):
                        if path[i] == "r" and path[i + 1] == "o":
                            root_name = path[i:]
                            break
                    debounces["kill_root"] += 1
                    QTimer.singleShot(25000, lambda: partial(update_value, debounces["kill_root"], math.floor(debounces["kill_root"] - 1)))


                    if debounces["kill_root"] > 2:
                        self.send(f"[SERVER]> Too many attempts, Try again later", 2)
                    else:
                        if random.randint(0, terminate_root_chance) == terminate_root_chance:
                            self.send(f"[SERVER]> Terminating root '{root_name}'", 3)
                            core_dict.pop(path)
                            self.send(f"[SERVER]> Terminated root '{root_name}'", random.randint(20, 25))
                        else:
                            if random.randint(0, 25) == 25:
                                self.send(f"[SERVER]> Access denied with response: '{random.choice(root_terminate_denied_messages)}'", 4)
                            else:
                                self.send(f"[SERVER]> Access Denied", 2)
                else:
                    self.send(f"[SERVER]> Root '{path}' does not exist", 2)
                

            elif command.lower().startswith("pop_spore"):
                # Get spore information
                path = command[len("pop_spore") + 1:].lower()
                spore_name = ""

                for i in range(0, len(path) - 1):
                    if path[i] == "s" and path[i + 1] == "p":
                        spore_name = path[i:]
                        break
                
                root_path = path[:-len(spore_name) - 1]

                # Run command
                if path.startswith(core_loc) and root_path in core_dict:
                    
                    # Check if its already ruptured
                    if core_dict[root_path][spore_name]["status"] == spore_statuses[2]:
                        self.send(f"[SERVER]> Spore '{path}' is already ruptured", 2)
                    else:
                        core_dict[root_path][spore_name]["status"] = spore_statuses[2]

                        for j in range(1, random.randint(5, 20)):
                            addSpore(j, root_path)
                        self.send(f"[SERVER]> [ALERT] New spores detected on root '{root_path}'", random.randint(4, 8))

                        #if random.randint(1, spore_sprout_chance) == spore_sprout_chance:
                        #    core_dict[root_path][spore_name].update({"sub_root": {"path": f"{path}/{spore_name}_subroot"}})
                        #    core_dict[root_path][spore_name]["sub_root"].update({"spores": {}})
                        #    threading.Thread(target=process_subroot,args=(root_path, spore_name,)).start()
                        #    self.send(f"[SERVER]> [ALERT] New branch detected from spore '{spore_name}'", 35)

                        self.send(f"[SERVER]> Spore '{path}' popped", 3)
                else:
                    self.send(f"[SERVER]> Spore '{path}' does not exist", 2)


                        

            elif command.lower().startswith("init_root"):
                root_name = command[len("init_root") + 1:].lower()
                root_number = root_name[len("root_"):]
                root_path = f"{core_loc}{root_name}"

                if root_name.startswith("root_") and not root_number.isalpha() and not root_path in core_dict:
                    if uninitialized_roots > 1:
                        self.send(f"[SERVER]> Access denied", 2)
                    else:
                        core_dict[root_name] = None
                        threading.Thread(target=process_root, args=(root_path,)).start()

                        self.send(f"[SERVER]> Initializing root '{root_path}'", 2)
                        self.send(f"[SERVER]> Initialized root '{root_path}'", random.randint(60, 120))
                else:
                    self.send(f"[SERVER]> Invalid root '{root_path}'", 2)

            elif command.lower().startswith("observe"):
                m = command[len("observe") + 1:].lower()
                spore = ""

                # Get spore name
                for i in range(0, len(m)):
                    if m[i] == "s" and m[i + 1] == "p":
                        spore = m[i:]
                        break
                
                location = m[:-len(spore) - 1]
                if location in core_dict:
                    # Send out the spore's status.
                    status = core_dict[location][spore]["status"]
                    self.send(f"[SERVER]> Spore '{m}' Status: {status}", 2)
                else:
                    self.send(f"[SERVER]> Spore '{m}' does not exist", 2)
            else:
                self.send(f"[SERVER]> '{command}' is a unknown command", 2)
                    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
