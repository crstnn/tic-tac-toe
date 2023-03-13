# tic-tac-toe

Simple Tic Tac Toe game.

Features:
- Works for variable size boards (where length == height).
- _O(1)_ time complexity for state determination, on any given turn.
- Taking the board creation as a given, auxiliary space complexity is _O(n)_ on initial setup (where _n_ is the length of the board). This needed for constant time state determination.
- Set of simple unit tests with automated GitHub Actions testing.