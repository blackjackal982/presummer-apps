import click

@click.group()
@click.option('--removedigits/--no-removedigits','-rd/-nrd',default=False,help="remove digits")
@click.pass_context
def main(ctx,removedigits):
    ctx.obj['rd'] = removedigits

@main.command(help="concat string with delimiter")
@click.option('-d',default=':',help="default delim")
@click.argument('strings',nargs=-1)
@click.pass_context
def concat(ctx,d,strings):
    str_list = []
    if ctx.obj['rd'] == True:
        for i in strings:
            str_list.append("".join(j for j in i if not j.isdigit()))
        click.echo(str(d).join(str_list))
    else:
        click.echo(str(d).join(strings))

@main.command(help="convert the string to upper")
@click.argument('strings',nargs=-1)
@click.pass_context
def upper(ctx,strings):
    str_list = []
    if ctx.obj['rd'] == True:
        for i in strings:
            str_list.append("".join(j for j in i if not j.isdigit()))
        for i in str_list:
            click.echo(i.upper())
    else:
        for i in strings:
            click.echo(i.upper())


@main.command(help="convert the string to upper")
@click.argument('strings',nargs=-1)
@click.pass_context
def lower(ctx,strings):
    str_list = []
    if ctx.obj['rd'] == True:
        for i in strings:
            str_list.append("".join(j for j in i if not j.isdigit()))
        for i in str_list:
            click.echo(i.lower())
    else:
        for i in strings:
            click.echo(i.lower())

if __name__=='__main__':
    main(obj={})


