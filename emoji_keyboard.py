# requires pip install pynput
# If pip is not recognized, but python is installed, probably just need to add the python Scripts folder to path
    
alphabet = {
  "a": ":apple:",
  "b": ":bee:",
  "c": ":circus_tent:",
  "d": ":deer:",
  "e": ":elephant:",
  "f": ":fish:",
  "g": ":giraffe:",
  "h": ":heart:",
  "i": ":ice_cube:",
  "j": ":jellyfish:",
  "k": ":kite:",
  "l": ":lion_face:",
  "m": ":milk:",
  "n": ":nerd:",
  "o": ":octopus:",
  "p": ":pea_pod:",
  "q": ":flag_qa:",
  "r": ":rabbit:",
  "s": ":snake:",
  "t": ":t_rex:",
  "u": ":umbrella2: ",
  "v": ":volleyball:",
  "w": ":waffle:",
  "x": ":x_ray:",
  "y": ":yellow_square:",
  "z": ":zebra:",
  "!": ":exclamation:",
  "?": ":question:",
  "-": ":heavy_minus_sign:",
  "=": ":heavy_equals_sign:",
  " ": "     ",
  "\n": "\n",
  "+": ":heavy_plus_sign:"
}

while True:
    text = input(">").lower()
    out = "-# "
    for i in text:
        if i in alphabet.keys():
            out += alphabet[i] + " "
    print(out)
             