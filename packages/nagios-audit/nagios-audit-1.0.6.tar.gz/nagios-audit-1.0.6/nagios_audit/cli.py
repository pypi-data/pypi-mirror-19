import click
from presentation import Presentation

@click.command()
@click.option('--input_file', default='status.dat', help='Location of the nagios.stat file.')
@click.option('--output_file', default=None, help='Location of the output csv file')
def main(input_file, output_file):
    """Auditing tool for Nagios"""
    presentation_obj = Presentation(input_file)
    presentation_obj.printAll()
    if output_file != None:
        if presentation_obj.writeToFile(output_file):
            print("File %s saved successfully" % (output_file,))
        else:
            print("This is some problem in writing to file %s" % (output_file,))

if __name__ == '__main__':
    main()
