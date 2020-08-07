import discord 
from discord.ext import commands
from discord.utils import get
import os

client = commands.Bot( command_prefix = '.' )
client.remove_command('help')
bad_words = ['пидр', 'нигер', 'пидор', 'черный', 'пидарас', 'нигеры','хач','гей,']
stack = ['сетка']

connection = sqlite3.connect('server db')
cursor = connection.cursor()


@client.event
async def on_ready():
	cursor.execute("""CREATE TABLE if NOT EXISTS users (
		name TEXT,
		id INT,
		cash BIGINT,
		rep INT,
		lvl INT
	)""")
	connection.commit()

	cursor.execute("""CREATE TABLE if NOT EXISTS shop (
		role_id INT,
		id INT,
		cost BIGINT
	)""")

	for guild in client.guilds:
		async for member in guild.fetch_members():
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
				sql = f"""INSERT INTO users (name, id, cash, rep, lvl) VALUES ('{str(member.name).replace("'", "", 20)}', {member.id}, 0, 0, 1 )"""
				cursor.execute(sql)
				connection.commit()
			else:	
 				pass

	print ('bot connected')
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


	emb = discord.Embed( title = 'CIS команды ',colour = discord.Color.blue())
	emb.add_field(name = '**clear**',value = '```Очистка чата\n(для админов)```')
	emb.add_field(name = '**kick**',value = '```Кик пользователя\n(для админов)```')
	emb.add_field(name = '**ban**',value = '```Бан пользователя\n(для админов)```')
	emb.add_field(name = '**mute**',value = '```Мут пользователя\n(для админов)```')
	emb.add_field(name = '**award**',value = '```Выдать баллы\n(для админов)```')
	emb.add_field(name = '**take**',value = '```Забрать баллы\n(для админов)```')
	emb.add_field(name = '**addshop**',value = '```Добавить в магазин роль за баллы\n(для админов)```')
	emb.add_field(name = '**removeshop**',value = '```Убрать роль из магазина за баллы\n(для админов)```')
	emb.add_field(name = '**balance**',value = '```Посмотреть баланс```')
	emb.add_field(name = '**shop**',value = '```Посмотреть магазин```')
	emb.add_field(name = '**buy @роль**',value = '```купить роль```')
	emb.add_field(name = '**join**',value = '```В разработке```')
	emb.set_footer(text = 'Спасибо за использование нашего бота')
	emb.set_thumbnail(url = client.user.avatar_url)

	await ctx.send( embed = emb)
	
@client.command(pass_context = True)	
async def balance(ctx,member: discord.Member = None):
	await ctx.channel.purge( limit = 1)
	if member is None:

		sql = f"SELECT cash FROM users WHERE id = {ctx.author.id}"
		user_balance = cursor.execute(sql).fetchone()[0]
		await ctx.send(embed = discord.Embed(
			description = f"Баланс пользователя **{ctx.author}** составляет **{user_balance}**"))
	else:
		sql = f"SELECT cash FROM users WHERE id = {member.id}"
		user_balance = cursor.execute(sql).fetchone()[0]
		await ctx.send(embed = discord.Embed(
			description = f"Баланс пользователя **{member}** составляет **{user_balance}**"))


@client.command(pass_context = True)
@commands.has_permissions( administrator = True )
async def award(ctx,member: discord.Member = None, amount: int = None):

	if member is None:
		await ctx.send(f"**{ctx.author}**, укажите пользователя")
	else:
		if amount is None:
			await ctx.send(f"**{ctx.author}**, укажите сумму")
		elif amount < 1:
			await ctx.send(f"**{ctx.author}**, слишком маленькая сумма")
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount,member.id))
			connection.commit()

			await ctx.message.add_reaction('✅')

@client.command(pass_context = True)
@commands.has_permissions( administrator = True )
async def take(ctx,member: discord.Member = None, amount = None):
	
	if member is None:
		await ctx.send(f"**{ctx.author}**, укажите пользователя")
	else:
		if amount is None:
			await ctx.send(f"**{ctx.author}**, укажите сумму")
		elif amount == 'all':
			cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0,member.id))
			connection.commit()

			await ctx.message.add_reaction('✅')

		elif int(amount) < 1:
			await ctx.send(f"**{ctx.author}**, слишком маленькая сумма")
		else:
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount,member.id))
			connection.commit()

			await ctx.message.add_reaction('✅')



@client.command(pass_context = True)
@commands.has_permissions( administrator = True )
async def addshop(ctx,role: discord.Role = None, cost: int = None):
	if role is None:
		await ctx.send(f"**{ctx.author}**, укажите роль")
	else:
		if cost is None:
			await ctx.send(f"**{ctx.author}**, укажите стоимость")
		elif cost < 0:
			await ctx.send(f"**{ctx.author}**,стоимость не может быть меньше 0")
		else:
			cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id,cost))
			connection.commit()

			await ctx.message.add_reaction('✅')

@client.command(pass_context = True)
@commands.has_permissions( administrator = True )
async def removeshop(ctx,role: discord.Role = None):
	if role is None:
		await ctx.send(f"**{ctx.author}**, укажите роль")
	else:
		cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
		connection.commit()

		await ctx.message.add_reaction('✅')



@client.command(pass_context = True)
async def shop(ctx):
	embed = discord.Embed(title = 'Магазин ролей')

	for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
		if ctx.guild.get_role(row[0]) != None:
			embed.add_field(
				name = f"Стоимость **{row[1]}**:dollar:",
				value = f"Вы купите роль {ctx.guild.get_role(row[0]).mention}",
				inline = False 
			)
		else:
			pass
	await ctx.send(embed = embed)


@client.command(pass_context = True)
async def buy(ctx, role: discord.Role = None):
	if role is None:
		await ctx.send(f"**{ctx.author}**, укажите роль")
	else:
		if role in ctx.author.roles:
			await ctx.send(f"**{ctx.author}**, у вас есть такая роль")
		elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
			await ctx.send(f"**{ctx.author}**, у вас недостаточно средтсв для данной покупки,вы бомж")
		else:
			await ctx.author.add_roles(role)
			cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
			connection.commit()

			await ctx.message.add_reaction('✅')

	
#лив и заход
@client.event
async def on_member_join(member):
	if member.guild.id == 702819565385678878: # main
		guild = member.guild
		channel = discord.utils.find(lambda c: c.id == 702821220399448176, guild.text_channels)
		#role = discord.utils.get(member.guild.roles, id = 706516091190640651,)
		#await member.add_roles(role)
		await channel.send(f'**{member.mention}** залетает на сервер **{guild.name}**')

	elif member.guild.id == 653994383062073400: # essentenal
		guild = member.guild
		channel = discord.utils.find(lambda c: c.id == 653996740919296000, guild.text_channels)
		role = discord.utils.get(member.guild.roles, id = 653996061152509962,)
		await member.add_roles(role)
		await channel.send(f'**{member.mention}** залетает на сервер **{guild.name}**')

	elif member.guild.id == 537651980026249236: # kolins
		guild = member.guild
		channel = discord.utils.find(lambda c: c.id == 543154416367304704, guild.text_channels)
		#role = discord.utils.get(member.guild.roles, id = 653996061152509962,)
		#await member.add_roles(role)
		await channel.send(f'**{member.mention}** залетает на сервер **{guild.name}**')

	elif member.guild.id == 713145524018217010: # mafia server
		guild = member.guild
		channel = discord.utils.find(lambda c: c.id == 713146000734290021, guild.text_channels)
		role = discord.utils.get(member.guild.roles, id = 713149193169928274,)
		await member.add_roles(role)
		await channel.send(f'**{member.mention}** залетает на сервер **{guild.name}**')
		
	if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
		cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1)")
		connection.commit()
	else:
 		pass


@client.event
async def on_member_leave(member):
	if member.guild.id == 537651980026249236:
		guild = member.guild
		channel = discord.utils.find(lambda c: c.id == 702821220399448176, guild.text_channels)
		await channel.send(f'**{member.mention}** съебался с нашего сервака **{guild.name}**')

	elif member.guild.id == 713145524018217010: # maf
		guild = member.guild
		channel = discord.utils.find(lambda c: c.id == 713146000734290021, guild.text_channels)
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
	


		
		
@client.event
async def on_message(message):
	emb = discord.Embed( title = 'сетка', colour = discord.Color.green())
	await client.process_commands(message)


	msg = message.content.lower()

	if msg in stack:

		emb.set_image( url = 'https://media.discordapp.net/attachments/537651980026249240/706929888333922314/qeRlK051GMFsovYSDC5PCQ.jpeg?width=1204&height=677')

		await message.channel.send(embed = emb)

	if msg in bad_words:
		await message.delete()
		await message.channel.send(f'{message.author.mention} еще раз напишешь, кикну!')

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
