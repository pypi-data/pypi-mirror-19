import click
import csv

from manyquery.connection import Connection, MultiConnection


@click.command()
@click.option('--host', '-h', default=['ict.croptrak.com'], multiple=True,
                help='Hostname. Repeatable.')
@click.option('--user', '-u', help='MySQL username')
@click.option('--password', '-p', prompt=True, hide_input=True, 
                help='MySQL password')
@click.option('--database', '-d', multiple=True,
                help='Databases to execute query on. Default: all. Repeatable.')
@click.option('--all-hosts', help='Executes a query on all hostnames. ' \
                'Not compatible with --databases option.', is_flag=True)
@click.argument('infile', type=click.File('rb'))
@click.argument('outfile')
def cli(host, user, password, databases, all_hosts, infile, outfile):
    if databases and len(host) > 1:
        click.echo('--databases option only available when used with single host')
        return

    if all_hosts:
        conn = MultiConnection(user, password)
    elif len(host) > 1:
        conn = MultiConnection(user, password, host=host)
    else:
        conn = Connection(host[0], user, password)
        
    if databases:
        conn.select_dbs(databases)
        
    query = ''
    while True:
        chunk = infile.read(1024).decode('utf-8')
        if not chunk:
            break
        query = query + chunk
    query = [query.replace(char, ' ') for char in ['\n', '\t']]
    
    with open(outfile, 'w') as f:
        writer = csv.writer(f)
        for row in conn.execute(query, include_fields=True):
            writer.writerow(row)