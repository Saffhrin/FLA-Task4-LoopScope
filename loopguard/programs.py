"""Small example catalogue used by the command-line demonstration."""

EXAMPLES = {
    "countdown": "i = 6\nwhile i > 0:\n    i -= 1",
    "stuck": "i = 4\nwhile i < 9:\n    i -= 2",
    "skip-bound": "i = 1\nwhile i != 8:\n    i += 3",
    "unsupported": "i = 1\nwhile i < 10:\n    i += 1\n    print(i)",
}
