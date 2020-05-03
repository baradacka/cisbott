import discord 
from discord.ext import commands
from discord.utils import get
import os

client = commands.Bot( command_prefix = '.' )
client.remove_command('help')



@client.event

async def on_ready():
	print ( 'bot connected' )
	await client.change_presence(status = discord.Status.online, activity = discord.Game('шахте'))



#@client.command( pass_context = True )

#async def hello( ctx, amount = 1 ):

#	await ctx.channel.purge( limit = amount)

#	author = ctx.message.author
#	await ctx.send(f' { author.mention } Привет, я снг бот для дискорда ' )


@client.command(pass_context = True)

async def help(ctx):
	emb = discord.Embed( title = 'CIS команды ',colour = discord.Color.blue())

	await ctx.channel.purge( limit = 1)


	emb.add_field(name = '**clear**',value = '```Очистка чата\n(для админов)```')
	emb.add_field(name = '**kick**',value = '```Кик пользователя\n(для админов)```')
	emb.add_field(name = '**ban**',value = '```Бан пользователя\n(для админов)```')
	emb.add_field(name = '**mute**',value = '```Мут пользователя\n(для админов)```')
	emb.add_field(name = '**join**',value = '```В разработке```')
	emb.set_footer(text = 'Спасибо за использование нашего бота')
	emb.set_thumbnail(url = client.user.avatar_url)

	await ctx.send( embed = emb)

	
#лив и заход
@client.event
async def on_member_join(member):
	guild = member.guild
	channel = discord.utils.find(lambda c: c.id == 702821220399448176, guild.text_channels)
	await channel.send(f'**{member.mention}** залетает на сервер **{guild.name}**')
	
#eseentenal	
@client.event
async def on_member_join(member):
	guild = member.guild
	channel = discord.utils.find(lambda c: c.id == 653996740919296000, guild.text_channels)
	role = discord.utils.get(member.guild.roles, id = 653996061152509962,)
	await member.add_roles(role)
	await channel.send(f'**{member.mention}** залетает на сервер **{guild.name}**')


@client.event
async def on_member_leave(member):
	guild = member.guild
	channel = discord.utils.find(lambda c: c.id == 702821220399448176, guild.text_channels)
	await channel.send(f'**{member.mention}** съебался с нашего сервака **{guild.name}**')



#чат 

@client.command(pass_context = True)
@commands.has_permissions( administrator = True )

async def clear( ctx, amount : int):
	await ctx.channel.purge( limit = amount)

#@client.event 
#async def on_command_error(ctx, error):
#	pass

@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument ):
		await ctx.send(f'{ ctx.author.mention}, обязательно укажите сколько сообщений вы хотите удалить!')

	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ ctx.author.mention}, у вас недостаточно прав!')





#kick
@client.command(pass_context = True)
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
	emb = discord.Embed( title = 'КИК БЛЯТЬ', colour = discord.Color.red())
	await ctx.channel.purge( limit = 1)

	await member.kick( reason = reason)
	emb.set_author(name = member.name, icon_url = member.avatar_url)
	emb.add_field( name = 'КИК', value = 'КИКНУТ  : {}'.format(member.mention))
	emb.set_footer(text = 'БЫЛ КИКНУТ АДМИНОМ {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
	await ctx.send( embed = emb)

@kick.error
async def kick_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ ctx.author.mention}, у вас недостаточно прав!')


#ban
@client.command(pass_context = True)
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
	emb = discord.Embed( title = 'БАН БЛЯТЬ', colour = discord.Color.red())
	await ctx.channel.purge( limit = 1)

	await member.ban( reason = reason)
	emb.set_author(name = member.name, icon_url = member.avatar_url)
	emb.add_field( name = 'БАН', value = 'ЗАБАНЕН  : {}'.format(member.mention))
	emb.set_footer(text = 'БЫЛ ЗАБАНЕН АДМИНОМ {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
	await ctx.send( embed = emb)

@ban.error
async def ban_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ ctx.author.mention}, у вас недостаточно прав!')


#embed test
#@client.command(pass_context = True)

#async def time(ctx):
	
#	emb = discord.Embed( title = 'your title', colour = discord.Color.green())

#	emb.set_author( name = client.user.name, icon_url = client.user.avatar_url)
#	emb.set_footer(text = 'Cпасибо за использование нашего бота')
#	emb.set_image( url = 'https://bipbap.ru/wp-content/uploads/2017/10/0_8eb56_842bba74_XL-640x400.jpg')
#	emb.set_thumbnail(url = 'https://bipbap.ru/wp-content/uploads/2017/10/0_8eb56_842bba74_XL-640x400.jpg')

#	await ctx.send(embed = emb)

#mute

@client.command(pass_context = True)
@commands.has_permissions( administrator = True )

async def mute(ctx, member: discord.Member):
	await ctx.channel.purge( limit = 1)

	mute_role = discord.utils.get(ctx.message.guild.roles, name = 'MUTE')

	await member.add_roles( mute_role)
	await ctx.send(f'У {member.mention}, ограничение чата, потому что админам так захотелось!')

@mute.error
async def mute_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ ctx.author.mention}, у вас недостаточно прав!')

#message 
@client.command(pass_context = True)
async def send(ctx):
	await ctx.author.send('test')


#async def send1(ctx, member: discord.Member):
	#await member.send()

#voice

@client.command(pass_context = True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


@client.command(pass_context = True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()










#token = open( 'token.txt', 'r').readline()
token = os.environ.get('BOT_TOKEN')

client.run(str(token) )
