import json
import subprocess
import os
from pathlib import Path

# zeroth-order command-line interface from python (no real error checking etc..)

def_exe = r'C:\Program Files (x86)\Crossword Compiler\ccw.exe'
test_exe = r'C:\Users\micro\Documents\Rad Studio\Projects\ccwxe4\ccw.exe'


def run_commands(command_list: list[dict], exe_file=None, dump_file=None):
    exe_file = exe_file or (test_exe if os.path.exists(test_exe) else def_exe)
    if not os.path.exists(exe_file):
        raise FileNotFoundError(f"Crossword Compiler must be installed first.")
    command_dict = {'version': 1,
                    'commands': command_list}
    if dump_file:
        with open(dump_file, "w") as json_file:
            json.dump(command_dict, json_file, ensure_ascii=False, indent=4)
    input_str = json.dumps(command_dict, ensure_ascii=False).encode('utf-8')
    return subprocess.run([exe_file, '-c'], input=input_str, capture_output=True, check=True)


def convert_lst(file: str | Path, info: str = '', *, min_score=10, charset='utf-8',
                score_separator='\t', filter=True, outfile=None):
    """Convert a plain text word list (utf-8) to Crossword Compiler .lst format.

    :param file: Path to input text file
    :param info: Description text for the list. Defaults to filename if empty
    :param min_score: Minimum word score to include. Defaults to 10
    :param charset: Character set for word list output. Defaults to 'utf-8'
    :param score_separator: Character separating word and score. Defaults to tab
    :param filter: Apply character filtering. Defaults to True, to skip non-alphanumeric inputs
    :param outfile: Output path. Defaults to input path with .lst extension
    :return: subprocess.CompletedProcess: Result of command execution
    """
    file = str(file)
    command = {'command': 'convert_list',
               'options': {'infile': file,
                           'outfile': outfile or os.path.splitext(file)[0] + '.lst',
                           'min_score': min_score,
                           'info': info or 'List converted from %s' % os.path.basename(file),
                           'score_separator': score_separator,
                           'charset': charset,
                           'character_filter': 5 if filter else 0
                           }
               }
    return run_commands([command])


def fill(outfile, exe_file=None):
    """
    Minimal example to do a random fill of a fixed grid pattern.

    :param outfile: output .puz file (Across Lite, could be other formats)
    :param exe_file: optional non-default exe path
    :return: subprocess.CompletedProcess: Result of command execution
    """
    assert outfile.endswith('.puz')
    command = {'command': 'fill_grid',
               'options': {'outfile': str(outfile)}
               }
    return run_commands([command], exe_file=exe_file)


def test_fill():
    script_dir = Path(__file__).resolve().parent
    test_puz_path = script_dir.parent / 'tests' / 'test_from_python.puz'
    result = fill(str(test_puz_path.absolute()))
    print(result.stdout.decode('utf-8'))
    print(result.stderr.decode('utf-8'))


def test_convert_list():
    script_dir = Path(__file__).resolve().parent
    test_txt_path = script_dir.parent / 'tests' / 'Astronomy.txt'
    convert_lst(test_txt_path.absolute())


if __name__ == '__main__':
    test_fill()
    # convert_lst(r'z:\wordlist.txt', outfile=r'z:\wordlist.lst', min_score=10, charset='utf-8', filter=True)
