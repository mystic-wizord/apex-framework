from os import close
import click
import chevron

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

    database_required = click.prompt("Do you have a database instance? [Y/N]") == 'Y'
    click.echo(f"Database setup needed? {database_required}")

    with open('./mustache/project-data-file.mustache') as data_file:
        if database_required:
            mongodb_uri = click.prompt("Please provide your MongoDB URI string")
            rendered_mustache = chevron.render(data_file, { 'name': name, 'db_required': database_required, 'mongodb_uri': mongodb_uri } )
            click.echo(rendered_mustache)
        else:
            # while True:
                open_api_dir = click.prompt("Please provide the location of your OpenApi files")
                rendered_mustache = chevron.render(data_file, { 'name': name, 'db_required': database_required, 'apis': [ { 'open_api_dir': open_api_dir } ] } )
                click.echo(rendered_mustache)

if __name__ == "__main__":
    cli()