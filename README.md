# NKGAME
A PyGame extension library that adds useful features!

# About

NKGAME Is a module that allows features like buttons, rects, text boxes, in-game cameras, and randomly generated terrain to be easilly implemented into the PyGame library.

NKGAME streamlines all the busy work and allows for a more optimized version of PyGame that allows for many things to be automated for you. For example, NKGAME will automatically draw all rects added to the game. 

NKGAME has a in-game camera, that allows for a specific object or rect to be centered in the middle of the screen. This creates a perspective effect of a camera fosucsing on one specific object.

![giphy](https://github.com/NathanK4261/NKGAME/assets/78992074/1c1146b0-711e-4e30-baba-9c0ab001d955)

In this example, player 1 is the rect square, and the blue square is player 2. Player 1 is centered on the screen and player 2 can freely move in and out of the camera for player 1

NKGAME can create randomly generated terrains insanely fast.

![giphy2](https://github.com/NathanK4261/NKGAME/assets/78992074/e4570272-3a85-4b21-a4a2-f7683bdda055)

In this example, we see a randomly generated terrain. The player looks like he is moving across the terrain since the camera only shows what is surrounding the playerm and keeps the player in the middle of the screen.

NKGAME also has 2 modules called NKNET and NKSERVER. They are simplified version of the sockets python module they allow for a server and connection to be made more easilly, but I plan to add the ability to send serialized data and a more robust protocoll for the NKSERVER and NKNET modules so they are less prone to errors in buffer size and data loss.

I made an example game using NKGAME, NKNET, and the NKSERVER modules. There is no mechanics in the game, but it allows for a multiplayer game with randomly generated terrain and a loading screen. All made using these three modules.

![giphy3](https://github.com/NathanK4261/NKGAME/assets/78992074/f74d5230-9fd0-4316-8a80-6e495c541bc2)

If you would like a more in-depth explination of NKGAME, NKNET, and NKSERVER. I will be posting videos about each individual part of them on a youtube channel, stay tuned to when he videos come out. Ill keep this README updated
