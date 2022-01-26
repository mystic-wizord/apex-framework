import pathlib
import os
import pwd
import click
import chevron
import json
import yaml

@click.group()
def cli():
    """
    Thank you for using Apex Framework!
    """
    pass

@cli.command()
def init():
    click.echo(f"Initializing Apex!")

    pathlib.Path(f'./apex-framework').mkdir(parents=True, exist_ok=True)

    if pathlib.Path('/apex-framework/settings.json').is_file():
        click.echo("It seems that apex has already been initialized!")
    else:
        work_dir = click.prompt("Please state where you would like your main working directory to be")

        if not work_dir or not work_dir.strip() or len(work_dir) <= 0: 
            work_dir = '..'

        with open('./mustache/settings.mustache') as mustache:
            settings_mustache = chevron.render(mustache, { 'work_dir': work_dir } )
            settings_file = open('./apex-framework/settings.json', 'x')
            settings_file.write(settings_mustache)
            settings_file.close()

            os.system(f'sudo mv "./apex-framework" "/home/{get_username()}/apex-framework" -i')


@cli.command()
@click.argument('name')
def create(name: str = None):
    if name and name.strip() and len(name) > 0: 
        click.echo(f"Creating new application: {name}!")
    else:
        name = click.prompt("Please give your project a name")
        click.echo(f"Creating new application: {name}!")

    # This hasn't been implemented yet :(
    database_required = click.prompt("Do you have a database instance? [Y/N]") == 'Y'
    click.echo(f"Database setup needed? {database_required}")

    with open('./mustache/project-data-file.mustache') as data_file:
        if database_required:
            mongodb_uri = click.prompt("Please provide your MongoDB URI string")
            rendered_mustache = chevron.render(data_file, { 'name': name, 'db_required': database_required, 'mongodb_uri': mongodb_uri } )
            click.echo(rendered_mustache)
        else:
            open_api_dir = click.prompt("Please provide the location of your OpenApi files")
            rendered_mustache = chevron.render(data_file, { 'name': name, 'db_required': database_required, 'open_api_dir': open_api_dir } )
            click.echo(rendered_mustache)

    working_dir = get_working_dir()

    pathlib.Path(f'{working_dir}/{name}/api-definitions').mkdir(parents=True, exist_ok=True)
    app_definition_file = open(f'{working_dir}/{name}/application-manifest.json', 'x')
    app_definition_file.write(rendered_mustache)
    app_definition_file.close()


@cli.command()
@click.argument('name')
def build(name: str = None):
    click.echo(f"Building {name}!")

@cli.command()
@click.argument('name')
def purge(name: str = None):
    if name and name.strip() and len(name) > 0: 
        click.echo(f"Purging {name}!")
    else:
        name = click.prompt("Please enter the name of the application to purge")
        click.echo(f"Purging {name}!")

    working_dir = get_working_dir()

    pathlib.Path(f'{working_dir}/{name}').rmdir()

def get_working_dir():
    settings = open(f'/home/{get_username()}/apex-framework/settings.json',)
   
    # returns JSON object as a dictionary
    data = json.load(settings)
    return data['working-dir']

def get_username():
    return pwd.getpwuid(os.getuid())[0]

if __name__ == "__main__":
    cli()

# Commands for setup:
#  - virtualenv venv
#  - . venv/bin/activate