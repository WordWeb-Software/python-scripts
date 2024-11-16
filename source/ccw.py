import json
import subprocess
import os
from pathlib import Path

# zeroth-order fill command-line interface (no error checking etc..)

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


def convert_lst(file, info='', *, min_score=10, charset='utf-8',
                score_separator='\t', filter=True, outfile=None):
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
    assert outfile.endswith('.puz')
    command = {'command': 'fill_grid',
               'options': {'outfile': outfile}
               }
    return run_commands([command], exe_file=exe_file)


if __name__ == '__main__':
    script_dir = Path(__file__).resolve().parent
    test_puz_path = script_dir.parent / 'tests' / 'test_from_python.puz'
    fill(str(test_puz_path.absolute()))

    # convert_lst(r'z:\wordlist.txt', outfile=r'z:\wordlist.lst', min_score=10, charset='utf-8', filter=True)
