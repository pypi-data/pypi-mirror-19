# TODO

## Skeleton

- [ ] Make one branch for Tkinter projects, one branch for PyGTK projects, one branch for PyQT projects, ...
- [ ] Add docs/
- [ ] Add tests/
- [ ] Add common tools: travis, ...

## Version 1.0

- [ ] Highlight "winning squares" (using a lighter version of the winner player's color)
- [ ] Improve the game logic architecture (remove redundancies, ...)
- [ ] Add argparse options
    - GUI: --save, --save-path "..."
    - TUI: --save, --save-path "...", --quiet, --repeat N, --player1 "...", --player2 "..."
- [ ] Add a toolscript to display benchmark statistics (JSON files)
- [ ] Add "minimax" IA
- [ ] Add "montecarlo" IA
- [ ] Move "IA" code to pyai
- [ ] Run "IA" in a separate thread to avoid GUI lags
- [ ] Improve the documentation (sphinx) and the README.rst file
- [ ] Add the project on jdhp.org
- [ ] Test pypi installation instructions on several OS (Linux, MacOS, Windows)
- [ ] Improve GUI (colors, ...)

## Version 1.0+

- [ ] Add IA:
    - MCTS
    - Alpha/Beta
    - DPS (with neural networks)
    - ...

