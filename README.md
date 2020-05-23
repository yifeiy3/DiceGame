# DiceGame
Online two player Chinese dice drinking game, did it so that people can play these over zoom to drink during coronavirus times. Implemented using `pygame`. The package is required to run the game.

# Run the Game
First, start the server running:
```
    python3 server.py
```
Then, people can join the game by running client file:
```
    python3 interface.py
```
One can optionally input username, and can create/join rooms. An spectator feature is also included.

# Rules of the Game
**Details: https://en.wikipedia.org/wiki/Liar%27s_dice**

The game is called liar's dice, where each player rolls 5 dies, each knowing their own dice values but not the others, and is trying to guess the total amount of one individual face value for both players.

Each player takes turns, and guess the total amount. For each guess, the player would either need to increase the amount of the face value or increase the total amount to guess, or both. An example is P1 guesses "3 Fours", then P2 can guess "3 x", where x can be 5 or 6, or "x y", where x > 3, and y can be any number.

In the game, `1` is a flex number, which is counted for any number in the guessing game. However, people can choose to not count 1's in total by calling `zhai`. When `zhai` is called, `1` can only represent `1` and not any other number. When player guesses about total number of `1`'s, zhai is required. The normal game state where `1` can count as any number is called `fei`.

One can transition from `fei` state fo `zhai` state by calling `zhai` with any number of an amount that is at least 1 less than the current state. And one can return from `zhai` to `fei` by calling any number with at least 2 more. In `zhai` state, `1` is considered the biggest face value. An example is P1 guess "3 Four Fei", then P2 can guess "x y zhai", where x >= 2 and y can be any amount. If P2 guess "2 Four zhai", then p1 can guess "x y fei", where x >= 4 and y can be any amount.

If all five dices are rolled to be the same facevalue, its called a `pure bao zi`, which counts for `7` of that face value under any condition. If all five dices are rolled to be either the same face value or `1`, its called a `bao zi`, which counts for `6` of the face value, when under `fei`.

The game starts with `fei` state and total amount of `3`, so you cant say anything less than `3 fei` in the first guess. When a player believes the total amount guess is greater than the current total amount, the player can `open`. The system will do a checksum to see whether

```
    total amount < guessed value
```
If true, the player who `open` wins. Otherwise the player loses. The loser will get to call first for the next round.
