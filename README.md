# Slagalica

A multiplayer clone of the popular regional TV quiz show "Slagalica", built entirely in Python using the `pygame` library. This project features a client-server architecture, allowing two players to compete against each other over a local network or the internet in real-time.

## Mini-games included

The game smoothly transitions through 6 classic mini-games:
1. **Slagalica (Word puzzle):** Form the longest possible word from a given set of random letters.
2. **Moj Broj (My number):** Use arithmetic operations and given numbers to reach a randomly generated target number. Includes dynamic solving logic.
3. **Skočko (Mastermind):** Deduce the correct combination of 4 symbols within a limited number of attempts.
4. **Spojnice (Connections):** Connect related terms from two separate columns.
5. **Ko zna, zna (Trivia quiz):** A general knowledge multiple-choice quiz. Questions are dynamically loaded from a local text file.
6. **Asocijacije (Associations):** Open fields in a 4x4 grid to guess column solutions and the final overarching answer.

## Features

* **Multiplayer System:** Built using Python's `socket` library. A central server coordinates the connection between two clients and synchronizes the scores in real-time.
* **Dynamic Module Loading:** The main game loop dynamically imports and runs each mini-game as an independent module using `importlib`, keeping the codebase modular and clean.
* **Custom UI:** Custom Pygame UI elements, including timers, animated buttons, and gradient visuals.

## Prerequisites

To run this game, you need Python 3.x and the `pygame` library installed:

```bash
pip install pygame
