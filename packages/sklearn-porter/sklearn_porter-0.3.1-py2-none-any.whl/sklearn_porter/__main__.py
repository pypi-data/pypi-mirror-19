# -*- coding: utf-8 -*-

import os
import argparse

from . import Porter


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Transpile trained scikit-learn models '
            'to C, Java, JavaScript and others. '),
        epilog=(
            'More details on: '
            'https://github.com/nok/sklearn-porter'))
    parser.add_argument(
        '--input', '-i',
        required=True,
        help=(
            'Set the path of an exported model '
            'in pickle (.pkl) format.'))
    parser.add_argument(
        '--output', '-o',
        required=False,
        help='Set the destination directory.')
    parser.add_argument(
        '--language', '-l',
        choices=['c', 'java', 'js', 'go', 'php', 'ruby'],
        default='java',
        required=False,
        help=(
            'Set the target programming language '
            '("c", "java", "js", "go", "php", "ruby").'))
    args = vars(parser.parse_args())

    model_path = str(args['input'])
    if model_path.endswith('.pkl') and os.path.isfile(model_path):
        # Load data:
        from sklearn.externals import joblib
        raw_model = joblib.load(model_path)
        # Port model:
        porter = Porter(language=str(args['language']), with_details=True)
        result = porter.port(raw_model)
        filename = result.get('filename')
        # Define destination path:
        if str(args['output']) != '' and os.path.isdir(str(args['output'])):
            model_path = str(args['output'])
            model_path = os.path.join(model_path, filename)
        else:
            model_path = model_path.split(os.sep)
            # if len(model_path) > 1:
            del model_path[-1]
            model_path += [filename]
            model_path = os.sep.join(model_path)
        # Save ported model:
        with open(model_path, 'w') as f:
            f.write(result.get('model'))
    else:
        raise ValueError('No valid model in pickle format was found.')

if __name__ == "__main__":
    main()
