from subprocess import run, Popen, PIPE
from typing import List
import glob
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os

from seaborn.palettes import color_palette

def clear_results(result_dir:str) -> None:
    files = glob.glob(os.path.join(result_dir, '*'))
    for f in files:
        os.remove(f)

def init_playground(bmark_dir: str, result_dir: str) -> None:
    run(["cp", bmark_dir, result_dir])

def run_abc_commmand(abc_dir: str, input_dir:str, output_dir:str, command_str:str) -> List:
    command = [abc_dir]
    command.append('-c')
    abc_commands = [
        "read_blif "+input_dir,
        "source utils/abc.rc",
        "strash",
        command_str,
        "print_stats",
        "write_blif "+output_dir if output_dir != "" else ""
    ]
    command.append(';'.join(abc_commands))
    proc = Popen(command, stdout=PIPE)
    result = proc.communicate()[0].decode('utf-8')
    area_str, lev_str = result.split('=')[-2:]
    area = int(area_str.split()[0].strip())
    lev = int(lev_str.strip())
    return area, lev

def get_abc_status(abc_dir: str, input_dir:str) -> List:
    return run_abc_commmand(abc_dir, input_dir, '', '')

def plot_area_vs_iteraton(csv_dir: str, figure_dir: str):
    df = pd.read_csv(csv_dir)
    initial_area = df[df['iteration']==0]['area'].mean()
    df['adjusted_area'] = df.apply(lambda x:
        x['area']/initial_area, axis=1)
    plt.rcParams.update({'font.size': 18, 'font.family':'serif'})

    plt.figure(figsize=(20, 6), dpi=80)
    plt.title('converge curve of different scripts') 
    plt.ylabel('circuit area')
    plt.xlabel('iterations (#)')

    plt.subplots_adjust(bottom=0.1, left=0.1)

    ax = sns.lineplot(data=df, x='iteration', y='adjusted_area', hue='command', palette='icefire')
    plt.savefig(figure_dir)
    return ax
