import os
import click
import chevron
import json

@click.group()
def cli():
    """
    Thank you for using Apex Framework!
    """
    pass


@cli.command()
@click.argument('name')
def init(name: str = None,):
    if name and name.strip() and len(name) > 0: 
        click.echo(f"Initializing {name}!")
    else:
        name = click.prompt("Please give your project a name")
        click.echo(f"Initializing {name}!")

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

    json_file = json.loads(rendered_mustache)

    app_dir = json_file['name']
    os.mkdir(f'../{app_dir}')

if __name__ == "__main__":
    cli()