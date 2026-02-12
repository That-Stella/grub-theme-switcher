import os

def casefold_sort(i):
    return i.casefold()

if os.geteuid() != 0:
    exit("You need root to update your themes!")

themes = os.listdir("/boot/grub/themes")
themes.sort(key=casefold_sort)
current_theme = ""
drop_in_config = True
GRUB_CONFIG_DIR = "/etc/default/grub.d/10-theme.cfg"

try:
   with open(GRUB_CONFIG_DIR, "r") as config:
        config_file = config.read()
        split_config = config_file.split("/")
        current_theme = split_config[4]
except:
    drop_in_config = False
    GRUB_CONFIG_DIR = "/etc/default/grub"
    with open(GRUB_CONFIG_DIR, "r") as config:
        config_file = config.read()
        for line in config_file.split("\n"):
           if "GRUB_THEME=" in line:
                theme_line = line
                break
        split_theme_line = theme_line.split("/")
        if len(split_theme_line) == 6:
            current_theme = split_theme_line[4]

print("These are the available themes:")
for i in range(len(themes)):
    if themes[i] == current_theme:
        print(f"{i+1}) {themes[i]} [Installed]")
    else:
        print(f"{i+1}) {themes[i]}")
selected_theme = int(input("Select a theme to install: ")) - 1

while selected_theme >= len(themes) or selected_theme < 0:
    selected_theme = int(input("Invalid theme number. Try again: ")) - 1
while themes[selected_theme] == current_theme:
    selected_theme = int(input(f"{current_theme} is already installed! Select another one: ")) - 1

if drop_in_config:
    with open(GRUB_CONFIG_DIR, "w") as config:
        config.write(f"GRUB_THEME=\"/boot/grub/themes/{themes[selected_theme]}/theme.txt\"\n")
else:
    sed_command = f"s/GRUB_THEME=*.*/GRUB_THEME=\"\/boot\/grub\/themes\/{themes[selected_theme]}\/theme.txt\"\\n/"
    fork = os.fork()
    if fork == 0:
        os.execlp("sed", "sed", "-i", sed_command, GRUB_CONFIG_DIR)

os.execlp("grub-mkconfig", "grub-mkconfig", "-o", "/boot/grub/grub.cfg")
