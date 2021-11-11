import click
##  TO DO LIST:
##  LEARN GIT COMMIT AND GIT CHECKPOINTS
##  LEARN PDB FOR DEBUGGING
##
##
##
@click.group()
@click.pass_context
def main(ctx):
    pass

@main.command(short_help="sercret help")
@click.option("-u","--username",prompt=True,help = "username whose secret is desired")
@click.option("-p","--password",prompt=True,hide_input=True,help="password for user whose secret desired",confirmation_prompt=True)
@click.pass_context
def secret(ctx,username,password):
    """secret command"""
    click.echo("\033[92m"+"secret for "+username+" is "+password+"\033[0m")


if __name__ =="__main__":
    main()
