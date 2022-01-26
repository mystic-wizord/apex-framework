import pathlib
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

    pathlib.Path(f'../{name}/api-definitions').mkdir(parents=True, exist_ok=True)
    app_definition_file = open(f'../{name}/application-manifest.json', 'x')
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

    pathlib.Path(f'../{name}').rmdir()


if __name__ == "__main__":
    cli()

# Commands for setup:
#  - virtualenv venv
#  - . venv/bin/activate