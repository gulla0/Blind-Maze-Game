
# Blind Maze Explorer

Welcome to **Blind Maze Explorer**, an engaging and challenging 2D maze game where you navigate through an invisible maze, uncovering walls as you collide with them. Test your memory and reflexes to reach the goal in 30 seconds per level! This game is built with Grok 3.

## Getting Started

Follow these steps to clone the repository, install dependencies, and start playing the game.

### Prerequisites

- **Python 3.8+**: Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **Git**: If you don’t have Git, download it from [git-scm.com](https://git-scm.com/downloads).

### Installation

1. **Clone the Repository**
   Open your terminal or command prompt and run the following command to clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/blind-maze-explorer.git
   ```

   Replace `your-username` with your GitHub username and `blind-maze-explorer` with the actual repository name if different.

2. **Navigate to the Project Directory**
   Change into the cloned directory:

   ```
   cd blind-maze-explorer
   ```

3. **Install Dependencies**
   This project requires the `pygame` library. Install it using pip:

   ```
   pip install pygame
   ```

   Ensure you have an internet connection to download the package.

### Running the Game

1. **Start the Game**
   Run the game script using Python:

   ```bash
   python3 blind_maze.py
   ```

   Replace `blind_maze.py` with the actual filename of the game script if it’s different.

2. **Play the Game**
   - You’ll see an initial screen with a “Play” button. Click it to start.
   - Use the **Arrow Keys** to move the player (a blue triangle) toward the “GOAL” (marked by a checkered flag) within 30 seconds per level.
   - Walls are invisible until you hit them—they flash subtly and leave a permanent border to help you remember.
   - Reach the goal to advance to the next level (grids get larger). If time runs out, see your score (final level - 1) and choose “Replay” or “End.”

### Notes

- The game runs in fullscreen mode for the best experience. Press `Esc` to exit at any time.
- If you encounter issues, ensure Python and Pygame are correctly installed. Check the console for error messages.
- This is an open-source project—feel free to contribute, report issues, or suggest improvements on GitHub!

### License

This project is open-source under the [MIT License](LICENSE) (or specify your chosen license here). See the `LICENSE` file for details.

### Acknowledgments

Thanks to the Pygame community for providing the tools to create this game, and to all contributors for making it fun and accessible!

---

Happy exploring, and good luck navigating the invisible maze!


