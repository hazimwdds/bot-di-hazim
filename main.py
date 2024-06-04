import discord
from discord.ext import commands, tasks
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Comandi di moderazione
@bot.slash_command(name="kick", description="Espelle un utente")
@commands.has_permissions(kick_members=True)
async def kick(ctx: discord.ApplicationContext, member: discord.Member, reason: str = None):
    await member.kick(reason=reason)
    await ctx.respond(f'{member} è stato espulso. Motivo: {reason}', ephemeral=True)

@bot.slash_command(name="ban", description="Banna un utente")
@commands.has_permissions(ban_members=True)
async def ban(ctx: discord.ApplicationContext, member: discord.Member, reason: str = None):
    await member.ban(reason=reason)
    await ctx.respond(f'{member} è stato bannato. Motivo: {reason}', ephemeral=True)

@bot.slash_command(name="clear", description="Elimina un certo numero di messaggi")
@commands.has_permissions(manage_messages=True)
async def clear(ctx: discord.ApplicationContext, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.respond(f'{amount} messaggi sono stati eliminati.', ephemeral=True)

@bot.slash_command(name="timeout", description="Mette un utente in timeout")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx: discord.ApplicationContext, member: discord.Member, duration: int, reason: str = None):
    await member.timeout(reason=reason, duration=duration)
    await ctx.respond(f'{member} è stato messo in timeout per {duration} secondi. Motivo: {reason}', ephemeral=True)

@bot.slash_command(name="tempban", description="Banna temporaneamente un utente")
@commands.has_permissions(ban_members=True)
async def tempban(ctx: discord.ApplicationContext, member: discord.Member, duration: int, reason: str = None):
    await member.ban(reason=reason)
    await ctx.respond(f'{member} è stato bannato per {duration} secondi. Motivo: {reason}', ephemeral=True)

    await asyncio.sleep(duration)
    await ctx.guild.unban(member)
    await ctx.send(f'{member} è stato sbannato dal server {ctx.guild.name}.')

# Nuovi comandi aggiunti
@bot.slash_command(name="mute", description="Silenzia un utente")
@commands.has_permissions(manage_roles=True)
async def mute(ctx: discord.ApplicationContext, member: discord.Member, reason: str = None):
    pass

@bot.slash_command(name="unmute", description="Rimuove il silenzio da un utente")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx: discord.ApplicationContext, member: discord.Member):
    pass

@bot.slash_command(name="warn", description="Avverte un utente")
@commands.has_permissions(kick_members=True)
async def warn(ctx: discord.ApplicationContext, member: discord.Member, reason: str = None):
    pass

@bot.slash_command(name="warns", description="Mostra i warning di un utente")
@commands.has_permissions(kick_members=True)
async def warns(ctx: discord.ApplicationContext, member: discord.Member):
    pass

@bot.slash_command(name="report", description="Segnala un utente")
async def report(ctx: discord.ApplicationContext, member: discord.Member, *, reason: str):
    report_channel_id = 1246444229610176513  # Sostituisci con l'ID del canale report
    report_channel = bot.get_channel(report_channel_id)
    if report_channel:
        report_message = f"**Segnalazione da {ctx.author.mention}:**\n\n"
        report_message += f"Utente segnalato: {member.mention}\n"
        report_message += f"Motivo: {reason}"
        await report_channel.send(report_message)
        await ctx.respond("Segnalazione inviata con successo.", ephemeral=True)
    else:
        await ctx.respond("Non è stato possibile trovare il canale di report.", ephemeral=True)
    pass 

@bot.slash_command(name="suggest", description="Invia una proposta/suggerimento")
async def suggest(ctx: discord.ApplicationContext, suggestion: str):
    suggestion_channel_id = 1246474416758460438  # Sostituisci con l'ID del canale suggerimenti
    suggestion_channel = bot.get_channel(suggestion_channel_id)
    if suggestion_channel:
        await suggestion_channel.send(f'Nuova proposta/suggerimento da {ctx.author.mention}: {suggestion}')
        await ctx.respond('Suggerimento inviato con successo.', ephemeral=True)
    else:
        await ctx.respond('Non è stato possibile trovare il canale suggerimenti.', ephemeral=True)
    pass

@bot.slash_command(name="userinfo", description="Mostra le informazioni su un utente")
async def userinfo(ctx: discord.ApplicationContext, member: discord.Member):
    roles = [role.mention for role in member.roles[1:]]  # Escludi @everyone
    embed = discord.Embed(title=f"Informazioni su {member}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Ruoli", value=", ".join(roles) if roles else "Nessuno", inline=True)
    embed.add_field(name="Account creato il", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    embed.add_field(name="Entrato nel server il", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    # Aggiungi altre informazioni come kick e ban se disponibili (non gestite da discord.py direttamente)
    await ctx.respond(embed=embed, ephemeral=True)
    pass

@bot.slash_command(name="serverinfo", description="Mostra le informazioni sul server")
async def serverinfo(ctx: discord.ApplicationContext):
    server = ctx.guild
    embed = discord.Embed(title=f"Informazioni su {server.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=server.icon.url)
    embed.add_field(name="ID", value=server.id, inline=True)
    embed.add_field(name="Proprietario", value=server.owner.mention, inline=True)
    embed.add_field(name="Membri totali", value=server.member_count, inline=True)
    embed.add_field(name="Numero di canali", value=len(server.channels), inline=True)
    embed.add_field(name="Server creato il", value=server.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    await ctx.respond(embed=embed, ephemeral=True)
    pass

@bot.slash_command(name="ping", description="Controlla la latenza del bot")
async def ping(ctx: discord.ApplicationContext):
    latency = bot.latency
    await ctx.respond(f'Pong! Latenza: {latency * 1000:.2f}ms', ephemeral=True)
    pass

@bot.slash_command(name="say", description="Fai dire qualcosa al bot")
async def say(ctx: discord.ApplicationContext, *, message: str):
    await  ctx.respond(message, ephemeral=True)
# Evento quando il bot è pronto
@bot.event
async def on_ready():
    print(f'Siamo entrati come {bot.user}')

