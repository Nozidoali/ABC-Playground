from dotenv import load_dotenv
load_dotenv()

import os
ABC_EXEC = os.getenv('ABC_EXEC')
EXP_HOME = os.getenv('EXP_HOME')

import sys
sys.path.append(EXP_HOME)
from utils.utils import get_abc_status, init_playground, plot_area_vs_iteraton, run_abc_commmand, clear_results

if __name__ == '__main__':

    result_dir = os.path.join(EXP_HOME, 'results')
    bmark_dir  = os.path.join(EXP_HOME, 'bmarks', 'example.blif')
    figure_dir = os.path.join(EXP_HOME, 'figures', 'e2.png')
    data_dir   = os.path.join(EXP_HOME, 'data')

    csv_dir    = os.path.join(data_dir, 'e2.csv')
    skip_data = os.path.exists(csv_dir)

    command_str_all = ['rwz;rf -z -N 15 -l 0; rs -K 16 -N 3 -l 0', 'rwz; rfz; rs', 'compress2rs']
    if skip_data == False:
        if os.path.exists(data_dir) == False:
            os.mkdir(data_dir)
        if os.path.exists(result_dir) == False:
            os.mkdir(result_dir)
        clear_results(result_dir)
        with open(csv_dir, 'w') as f:
            f.write('{},{},{},{}\n'.format('iteration', 'area', 'lev', 'command'))
            for command_str in command_str_all:
                iteration = 0
                iteration_step = 20 if command_str == 'compress2rs' else len(command_str.split(';')) if ';' in command_str else 1
                init_playground(bmark_dir, os.path.join(result_dir, '{}_{}.blif'.format
                        (command_str.replace(';','_').replace(' ', '-'), iteration)))
                prev_area, prev_lev = get_abc_status(ABC_EXEC, bmark_dir)
                useless_iteration = 0
                while True:
                    f.write('{},{},{},\"{}\"\n'.format(iteration, prev_area, prev_lev, command_str))
                    input_name = os.path.join(result_dir, '{}_{}.blif'.format
                        (command_str.replace(';','_').replace(' ', '-'), iteration))
                    output_name = os.path.join(result_dir, '{}_{}.blif'.format
                        (command_str.replace(';','_').replace(' ', '-'), iteration+iteration_step))
                    area, lev = run_abc_commmand(ABC_EXEC, input_name, output_name, command_str)
                    if area == prev_area and lev == prev_lev:
                        useless_iteration += iteration_step
                    else:
                        useless_iteration = 0
                    if useless_iteration >= 20:
                        break
                    prev_area, prev_lev = area, lev
                    iteration += iteration_step

    plot_area_vs_iteraton(csv_dir, figure_dir)
    
