#!/bin/env python3

import time
import os
import shutil
import random
import re
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

def read_ascii_art(file_path):
  file_path = os.path.join(base_dir, file_path)
  try:
    with open(file_path, 'r') as file:
      return file.read()
  except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    return ""

separator = r"-- \{\{ .* \}\} --"

def lerp(a, b, t):
    return a * (1 - t) + b * t

def read_file(path):
    slide_art = read_ascii_art(path)
    slide_frames = re.split(separator, slide_art)
    slide_frames = [line for line in slide_frames if line != '']
    return slide_frames


def animate_sliding(delay_min=0.005, delay_max=0.015, max_padding=5):
    slide_frames = read_file("./animation-move")
    if not slide_frames or len(slide_frames) < 2:
        print("Error: Not enough frames to animate.")
        return
    slide_frame_lines = [frame.splitlines() for frame in slide_frames]

    max_line_width = max((len(line) for line in slide_frame_lines[0]), default=0)
    max_line_width2 = max((len(line) for line in slide_frame_lines[1]), default=0)
    terminal_width = shutil.get_terminal_size(fallback=(80, 20)).columns
    terminal_height = shutil.get_terminal_size(fallback=(80, 20)).lines

    paths = (
        list(range(-max_line_width, terminal_width + 1)),
        list(range(terminal_width - 1, (terminal_width - max_line_width2) // 2, -1))
    )

    top_padding_rand = random.randint(0, max_padding)

    def lerp(a, b, t):
        return a * (1 - t) + b * t

    for path_index, path in enumerate(paths):
       lines = slide_frame_lines[path_index]
       text_height = len(lines)
       top_padding = max(0, (terminal_height - text_height) // 2)
       for frame_index, frame in enumerate(path):
            clear()
            print("\n" * (top_padding_rand if (path_index == 0) else top_padding), end="")
            for line_index, line in enumerate(lines):
                padded_line = ' ' * max(0, frame) + line
                print(padded_line[max(0, -frame):terminal_width])
            t = frame_index / (terminal_width * (path_index + 1))
            delay = lerp(delay_min, delay_max, t)
            time.sleep(delay)


def get_top_padding_to_center(lines):
    text_height = len(lines)
    terminal_size = shutil.get_terminal_size(fallback=(80, 24))
    terminal_height = terminal_size.lines
    top_padding = max(0, (terminal_height - text_height) // 2)

    terminal_width = terminal_size.columns
    longest_line_length = max((len(line) for line in lines), default=0)
    padding_left = (terminal_width - longest_line_length) // 2

    return padding_left, top_padding



def animate_centered_text(delay=0.7):
    texts = read_file("./animation-center")

    for i, text in enumerate(texts):
        lines = text.splitlines()

        clear()

        left_padding, top_padding = get_top_padding_to_center(lines)
        print("\n" * top_padding, end="")

        for line in lines:
            print(' ' * left_padding, end="")
            print(line)

        time.sleep(delay)

    last_text = texts[-1].splitlines()
    while len(last_text) > 0:
        last_text = last_text[:-1]
        clear()
        left_padding, top_padding = get_top_padding_to_center(last_text)
        print("\n" * top_padding, end="")
        for line in last_text:
            print(' ' * left_padding, end="")
            print(line)
        time.sleep(0.01)

def fire_animation():
    fire_frames: list[str] = read_file("./animation-fire")
    dance_frames = read_file("./animation-dance")

    dance_in_frames = read_file("./animation-dance-move")
    for i in range(len(fire_frames[0].splitlines()) - 4):
        lines = fire_frames[0].splitlines()
        lines = lines[len(lines) - i:]

        left_padding, top_padding = get_top_padding_to_center(lines)
        clear()
        print("\n" * top_padding, end="")

        for line in lines:
            print(' ' * left_padding, end="")
            print(line)

        animate_dance_if_fit(i, len(lines) + top_padding, dance_in_frames)
        
        time.sleep(0.15)

    dance_frame_index = 0
    for _frame_index, frame in enumerate(fire_frames):
        for i in range(2):
            lines = frame.splitlines()
            left_padding, top_padding = get_top_padding_to_center(lines)
            clear()
            print("\n" * top_padding, end="")

            for line in lines:
                print(' ' * left_padding, end="")
                print(line)

            animate_dance_if_fit(dance_frame_index % len(dance_frames), len(lines) + top_padding, dance_frames)
            dance_frame_index += 1

            time.sleep(0.15)

def animate_dance_if_fit(frame_index, prev_height, frames):
    terminal_height = shutil.get_terminal_size(fallback=(80, 24)).lines
    lines = frames[frame_index].splitlines()

    if prev_height + len(lines) > terminal_height:
        remove_lines = prev_height + len(lines) - terminal_height
        lines = lines[:-remove_lines]

    height_view = terminal_height - prev_height
    padding_top = max(0, (height_view - len(lines)) // 2)
    print("\n" * padding_top, end="")
    for line in lines:
        print(line)

def print_colored_stacktrace(trace: str):
    RED = '\033[31m'
    CYAN = '\033[36m'
    YELLOW = '\033[33m'
    DIM = '\033[2m'
    RESET = '\033[0m'

    for line in trace.splitlines():
        # Highlight exception messages
        if re.match(r'^\w.*Exception', line) or re.match(r'^\s*Caused by:', line):
            # hightlight "`command`" in exception messages
            line = re.sub(r'`([^`]+)`', YELLOW + r'`\1`' + RED, line)
            print(RED + line + RESET)
            continue

        # Highlight 'at' lines
        at_match = re.match(r'^(\s*)at\s+(.+?)\((.+?)\)', line)
        if at_match:
            indent, location, file_info = at_match.groups()
            # Highlight file info like MyClass.java:123
            file_info = re.sub(r'(\.java:\d+)', YELLOW + r'\1' + CYAN, file_info)
            print(f"{indent}{CYAN}at {location}({file_info}){RESET}")
            continue

        # Highlight suppressed or omitted lines
        if "Suppressed:" in line or "... " in line:
            print(DIM + line + RESET, end="")
            sys.stdout.flush()
            continue

        # Default line
        print(line)

def print_colored_traceback():
    stacktrace = """
    java.lang.OverdoseException: Cannot invoke "Main.continue(). Waiting 20s..."
        at com.main.a.method(Main.java:23)
        at com.main.s.method(Main.java:06)
        at com.main.i.method(Main.java:2025)
        at sh.ascii.r.Sh.main(Sh.java:)
        at sh.ascii.y.Animator.main(Animator.java:)
        at sh.ascii.k.Scene.show(Scene.java:)
    Caused by: java.!ang.IllegalBoredException: To get more info, please run `man brother` command.
        at com.example.Helper.check(Helper.java:45)
    ... 130 more"""

    print_colored_stacktrace(stacktrace)

def print_terminal_prompt(command: str, typing_delay: float = 0.15):
    YELLOW = '\033[33m'
    RESET = '\033[0m'

    # Print the directory line
    print(" (main) ~/home/Documents")

    # Print the prompt character with color
    sys.stdout.write(f" {YELLOW}{RESET} ")

    # Simulate human typing
    for char in command:
        sys.stdout.write(char)
        sys.stdout.flush()
        random_delay = random.uniform(typing_delay * 0.5, typing_delay * 1.5)
        time.sleep(random_delay)

    # Move to next line
    print()

def main():
  animate_sliding()
  animate_centered_text()
  fire_animation()
  print_colored_traceback()
  time.sleep(20)
  print("^C")
  print_terminal_prompt("man brother asiryk")

if __name__ == "__main__":
  main()
