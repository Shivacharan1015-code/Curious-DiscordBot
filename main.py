from asyncio.tasks import wait
import discord
from discord import message
from discord.embeds import Embed
import discord_slash
import requests
import json
import random
import datetime
import bs4
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option
client = commands.Bot(command_prefix=['~','-'])
# Beggining of Inspire Command --------------------------
slash = SlashCommand(client,sync_commands=True)
def inspire_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    author = json_data[0]['a']
    embbed = discord.Embed(title=quote, description=" By {}".format(author),color=0xCEB8FA)

    return embbed



@client.command(brief='~inspire', description='Returns a random inspirational quote')
async def inspire(context):
    print('Inspire Command' + str(datetime.datetime.now()) + ' ' +context.author.name)
    wait_msg = await context.send("{}".format(context.author.mention))
    await wait_msg.edit(embed=inspire_quote())
    await wait_msg.add_reaction('👍')
    await wait_msg.add_reaction('👎')

@slash.slash(description='Gives a random inspirational quote')
async def inspire(context):
    print('Inspire Command' + str(datetime.datetime.now()) + ' ' +context.author.name)
    wait_msg = await context.send("{}".format(context.author.mention))
    await wait_msg.edit(embed=inspire_quote())
    await wait_msg.add_reaction('👍')
    await wait_msg.add_reaction('👎')


# End of Inspire Command ----------------------------------

# Beggining of Wiki command -------------------------------

def wiki_commad(search_item):
    link1 = "https://en.wikipedia.org/wiki/{}".format(search_item)
    response = requests.get(link1)
    soup = bs4.BeautifulSoup(response.text,'lxml')
    tittle = soup.select('.firstHeading')[0]
    tittle = tittle.getText()
    # print(tittle)
    image = soup.select('.image')[0]
    link = 'https:' + image.img['src']
    para = soup.find_all('p')
    para = para[1].get_text()
    embbed = discord.Embed(title= tittle,description=para,url=link1,color=0xCEB8FA)
    embbed.set_image(url=link)
    return embbed

@client.command(brief='~wiki SEARCH_ITEM', description='Returns a wikipedia link along with an image and some info')
async def wiki(context,*,search_item="Steve_Jobs"):
    print('Wiki Command' + str(datetime.datetime.now()) + '{} '.format(search_item) +context.author.name)
    wait_msg = await context.send("Getting the wikipedia page...")
    search_item = search_item.replace(" ","_")
    try:
        await wait_msg.edit(embed=wiki_commad(search_item))
    except:
        await wait_msg.edit(content='```Looks like you entered a invalid search item, make sure you spelled it right. Or there is no wikipedia page about the topic you entered```' + context.author.mention)

@slash.slash(name='wiki',description='Gives you some info from wikipedia',options=[
    create_option(name="search_item ",description='Enter the search item',option_type=3,required=True)
])
async def wiki(context,search_item: str):
    print('Wiki Command' + str(datetime.datetime.now()) + '{} '.format(search_item) +context.author.name)
    wait_msg = await context.send("Getting the wikipedia page...")
    search_item = search_item.replace(" ","_")
    try:
        await wait_msg.edit(embed=wiki_commad(search_item))
    except:
        await wait_msg.edit(content='```Looks like you entered a invalid search item, make sure you spelled it right. Or there is no wikipedia page about the topic you entered```' + context.author.mention)

# End of Wiki command --------------------------------------

# Beggining of Dog command ---------------------------------

def dog_image():
    response = requests.get("https://dog.ceo/api/breeds/image/random").json()
    image_url = response['message']
    # response = requests.get("https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1").json()
    # fact = response[0]['fact']
    embbed = discord.Embed(title="Did you know",description="fact unavailabe ATM",color= 0xCEB8FA)
    embbed.set_image(url = image_url)
    return embbed

@client.command(brief='~dog', description='Returns a random dog image')
async def dog(context):
    print("Dog command" + str(datetime.datetime.now()) + ' ' +context.author.name)
    wait_msg = await context.send("Searching for a dog")
    await wait_msg.edit(content="Found one...")
    await wait_msg.edit(embed=dog_image())
    print("I'm in " + str(len(client.guilds)) + " servers!")

@slash.slash(name='dog',description='Gives a random dog image along with an intersting dog quote')
async def dog(context):
    print("Dog command" + str(datetime.datetime.now()) + ' ' +context.author.name)
    wait_msg = await context.send("Searching for a dog")
    await wait_msg.edit(content="Found one...")
    await wait_msg.edit(embed=dog_image())
    print("I'm in " + str(len(client.guilds)) + " servers!")

# End of Dog command ----------------------------------------

# Beggining of APOD command

def apod_image():
  nasa_key = 'Paste your NASA key here'
  response = requests.get("https://api.nasa.gov/planetary/apod?api_key={}".format(nasa_key))
  json_data = json.loads(response.text)
  # print(json_data)
  explanation = json_data['explanation']
  link = json_data['url']
  dat = json_data['date']
  title = json_data['title']
  media_type = json_data['media_type']
  embbed = discord.Embed(title="Link for image/video(click here)",description=explanation,color=0xCEB8FA,url=link)
  embbed.add_field(name="Date",value=dat,inline=True)
  embbed.add_field(name='Title',value=title,inline=True)
  embbed.add_field(name='Media Type',value=media_type,inline=True)
  embbed.set_image(url=link)
  return embbed

@client.command(brief='~apod', description='Returns a Astronomy picture of the day; Image provided by NASA, Updates every day[maynot be according to your local time]')
async def apod(context):
  print('Apod Command' + str(datetime.datetime.now()) + ' ' +context.author.name)
  msg = await context.send("Astronomy Picture of the day")
  await msg.edit(embed=apod_image())

@slash.slash(name='apod',description='Returns Astronomy picture of the day, along with some info about it, SOURCE: NASA')
async def apod(context):
  print('Apod Command' + str(datetime.datetime.now()) + ' ' +context.author.name)
  msg = await context.send("Astronomy Picture of the day")
  await msg.edit(embed=apod_image())
  

# End of APOD command ----------------------------------------------------------

#beggining of Food Command -----------------------------------------------------
def food_link(food_item):
    api_key = 'Paste your API key here, you can get it from spoonacular website'
    response = requests.get("https://api.spoonacular.com/recipes/search?query={1}&apiKey={0}".format(api_key,food_item))
    json_data = json.loads(response.text)
    total = json_data["number"] - 1
    recipe_number = random.randint(0,total)
    embbed = discord.Embed(title=json_data['results'][recipe_number]['title'] + "(Click Here)",url=json_data['results'][recipe_number]['sourceUrl'],description=str(json_data['results'][recipe_number]['readyInMinutes']) + 'min',color=0xCEB8FA)
    
    response = requests.get(json_data['results'][recipe_number]['sourceUrl'])
    soup = bs4.BeautifulSoup(response.text,'lxml')
    image = soup.find_all('img')
    image = image[6]['src']

    embbed.set_image(url=image)
    ing = ' '
    # try:
    item = soup.findAll('div', itemprop = "ingredients")
    for i in item:   
        ing += i.getText() + ' | '
    embbed.add_field(name='Ingredients',value=ing)
    # except:
    # embbed.add_field(name="Unable to fetch ingredients",value="Check website for more information")

    
    return embbed
def food_link_lite(food_item):
    api_key = 'Paste your API key here, you can get it from spoonacular website'
    response = requests.get("https://api.spoonacular.com/recipes/search?query={1}&apiKey={0}".format(api_key,food_item))
    json_data = json.loads(response.text)
    total = json_data["number"] - 1
    recipe_number = random.randint(0,total)
    embbed = discord.Embed(title=json_data['results'][recipe_number]['title'] + "(Click Here)",url=json_data['results'][recipe_number]['sourceUrl'],description=str(json_data['results'][recipe_number]['readyInMinutes'])+ 'min',color=0xCEB8FA)
    return embbed

@client.command(brief='~food FOOD_ITEM', description='Returns a recipe of the given food item, type in only one keyword for best results')
async def food(context,*,food_item='cake'):
    print('food Command' + str(datetime.datetime.now()) + ' {} '.format(food_item) +context.author.name)
    wait_msg = await context.send("Getting a tasty recipe for you...")
    try:
        await wait_msg.edit(embed=food_link(food_item))
        await wait_msg.add_reaction('❤️')
        await wait_msg.add_reaction('👍')
        await wait_msg.add_reaction('👎')
    except:
        try:
            await wait_msg.edit(embed=food_link_lite(food_item))
            await wait_msg.add_reaction('❤️')
            await wait_msg.add_reaction('👍')
            await wait_msg.add_reaction('👎')
        except:
            await wait_msg.edit(content="**There is no recipe for the given food item in my database :(** ```Try again with a different one```** Use only 1 keyword for best results: Ex Instead of 'Mini Nutella Cheesecakes' use 'cake'** ")

@slash.slash(name='food',description='Returns a recipie of the entered food item',options=[create_option(name='food_item',description='Enter the food item',option_type=3,required=True)])
async def food(context,food_item='cake'):
    print('food Command' + str(datetime.datetime.now()) + ' {} '.format(food_item) +context.author.name)
    wait_msg = await context.send("Getting a tasty recipe for you...")
    try:
        await wait_msg.edit(embed=food_link(food_item))
        await wait_msg.add_reaction('❤️')
        await wait_msg.add_reaction('👍')
        await wait_msg.add_reaction('👎')
    except:
        try:
            await wait_msg.edit(embed=food_link_lite(food_item))
            await wait_msg.add_reaction('❤️')
            await wait_msg.add_reaction('👍')
            await wait_msg.add_reaction('👎')
        except:
            await wait_msg.edit(content="**There is no recipe for the given food item in my database :(** ```Try again with a different one```** Use only 1 keyword for best results: Ex Instead of 'Mini Nutella Cheesecakes' use 'cake'** ")

# End of Food command -------------------------------------------------------------------------------------

# Beggining of Mars command -------------------------------------------------------------------------------
curiosity_names = ["fhaz","rhaz","mast","chemcam","mahli","mardi","navcam"]
def mars_image(date_data):
    nasa_key = 'Paste your nasa key here, you can get it from their API website, google {NASA API} '
    camera_name = random.choice(curiosity_names)
    response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={0}&api_key={1}}&camera={2}".format(date_data,nasa_key,camera_name))
    json_data = json.loads(response.text)
    embbed = discord.Embed(title=date_data,color=0xCEB8FA)
    embbed.add_field(name='Camera Name: ',value=json_data['photos'][0]['camera']['full_name'],inline=True)
    embbed.add_field(name='Rover Name: ',value=json_data['photos'][0]['rover']['name'],inline=True)
    embbed.add_field(name='Status: ',value=json_data['photos'][0]['rover']['status'],inline=True)
    embbed.set_image(url=json_data['photos'][0]['img_src'])

    return(embbed)


@client.command(brief='~mars EARTH_DATE[YYYY-MM-DD]', description='Returns a image taken by curiosity rover on mars on the earth date you provided, default date is 2020-10-15')
async def mars(context,date='2020-10-15'):
    print('Mars Command' + str(datetime.datetime.now()) + ' {} '.format(date) +context.author.name)
    wait_msg = await context.send("Searching...")
    for i in range(15):
      try:
        await wait_msg.edit(embed=mars_image(date))
        await wait_msg.edit(content=context.author.mention)
        await wait_msg.add_reaction('❤️')
        await wait_msg.add_reaction('👍')
        await wait_msg.add_reaction('👎')
        print("Sucess!!")
        break

      except:
        if(i>=12):
          error_msg = "**There is no picture on the date you provided**, ```Try the same command again, with different date,```** Make sure you enter date in the format YYYY-MM-DD, and the date should after 2014-08-18** Ex Command: ~mars 2020-10-15"
          await wait_msg.edit(content=error_msg)
          print("No Sucess!!")
          break

@slash.slash(name='mars',description='enter the date YYYY-MM-DD',options=[create_option(name='date',description='YYYY-MM-DD',option_type=3,required=True)])
async def mars(context,date='2020-10-15'):
    print('Mars Command' + str(datetime.datetime.now()) + ' {} '.format(date) +context.author.name)
    wait_msg = await context.send("Searching...")
    for i in range(15):
      try:
        await wait_msg.edit(embed=mars_image(date))
        await wait_msg.edit(content=context.author.mention)
        await wait_msg.add_reaction('❤️')
        await wait_msg.add_reaction('👍')
        await wait_msg.add_reaction('👎')
        print("Sucess!!")
        break

      except:
        if(i>=12):
          error_msg = "**There is no picture on the date you provided**, ```Try the same command again, with different date,```** Make sure you enter date in the format YYYY-MM-DD, and the date should after 2014-08-18** Ex Command: ~mars 2020-10-15"
          await wait_msg.edit(content=error_msg)
          print("No Sucess!!")
          break

# End of Mars command ------------------------------------------------------------------------------

# Start of ping command ----------------------------------------------------------------------------
@client.command()
async def ping(context):
    await context.send(" Ping is `{}` ms".format(round(client.latency * 1000)))

# End of ping command ------------------------------------------------------------------------------

# Start of earth command ---------------------------------------------------------------------------

def earth_image(lat,long,date):
    nasa_key = 'Paste your nasa key here, you can get it from their API website, google {NASA API} '
    response = requests.get('https://api.nasa.gov/planetary/earth/assets?lon={0}&lat={1}&date={2}&dim=0.10&api_key={3}'.format(lat,long,date,nasa_key))
    json_data = json.loads(response.text)
    try:
        embbed = discord.Embed(title=json_data['date'],description='If the image doesnt load, click on the title',url=json_data['url'])
        embbed.add_field(name='id: ',value=json_data['id'])
        embbed.add_field(name='service version',value=json_data['service_version'])
        embbed.set_image(url=json_data['url'])
    except:
        embbed = discord.Embed(title=json_data['msg'])
        embbed.add_field(name='service version',value=json_data['service_version'],inline=False)
    return embbed




@client.command(brief='~enter latitude, longitude and date, and the bot retrieves the Landsat 8 image for the supplied location and date')
async def earth(context,lat,long,date):
    print('Earth Command' + str(datetime.datetime.now()) + ' {0} {1} {2} '.format(lat,long,date) +context.author.name)
    wait_msg = await context.send("This command is still under development.")
    lat = float(lat)
    long = float(long)
    await wait_msg.edit(embed=earth_image(lat,long,date))
    await wait_msg.edit(embed=earth_image(lat,long,date))



# End of Earth command -------------------------------------------------------------------------------------

# Start of ps[people in space] command ---------------------------------------------------------------------

def ps_info():
    response = requests.get('http://api.open-notify.org/astros.json')
    json_data = json.loads(response.text)
    # print(json_data)
    total = json_data['number']
    json_data = json_data['people']
    embbed = discord.Embed(title='People In space: ',description='The names of all the people in space right now',color=0xCEB8FA)
    for i in range(0,total):
        embbed.add_field(name=json_data[i]['name'],value=json_data[i]['craft'],inline=True)
    embbed.add_field(name='Total number of people',value=str(total))

    return embbed


@client.command(brief='Returns the names of all the people in space right now',description='Returns the names of all the people in space right now')
async def ps(ctx):
    print('Ps Command' + str(datetime.datetime.now()) + ' ' +ctx.author.name)
    wait_msg = await ctx.send("Fetching the data")
    await wait_msg.edit(embed=ps_info())

@slash.slash(name='ps',description='gives you the names of all the people in space')
async def ps(ctx):
    print('Ps Command' + str(datetime.datetime.now()) + ' ' +ctx.author.name)
    wait_msg = await ctx.send("Fetching the data")
    await wait_msg.edit(embed=ps_info())
# End of ps[people in space command] ------------------------------------------------------------------------

# Start of iss command --------------------------------------------------------------------------------------
import time
def iss_coordinates(id=1):
    response = requests.get('http://api.open-notify.org/iss-now.json')
    json_data = json.loads(response.text)
    json_data = json_data['iss_position']
    if id == 1:
        embbed = discord.Embed(title='Current Co-ordinates of ISS',color=0xCEB8FA)
        embbed.add_field(name='Latitude',value=json_data['latitude'],inline=True)
        embbed.add_field(name='Longitude',value=json_data['longitude'],inline=True)

        return embbed
    else:
        embbed = discord.Embed(title='Co-ordinates of ISS at {}'.format(datetime.datetime.now()),color=0xCEB8FA)
        embbed.add_field(name='Latitude',value=json_data['latitude'],inline=True)
        embbed.add_field(name='Longitude',value=json_data['longitude'],inline=True)
        return embbed



@client.command(brief='Gives you the current co-ordinates of ISS',description='Gives the current co-cordinates of the International Space station')
async def iss(ctx):
    print('ISS Command' + str(datetime.datetime.now()) + ' ' +ctx.author.name)
    
    wait_msg = await ctx.send("Getting the co-codinates")
    start = 0
    while start < 5:
        await wait_msg.edit(content="LiveUpdate for 5 seconds")
        await wait_msg.edit(embed=iss_coordinates())
        start += 1
        time.sleep(1)

    await wait_msg.edit(embed=iss_coordinates(0))
@slash.slash(name='iss',description='gives you the co-ordinates of ISS')
async def iss(ctx):
    print('ISS Command' + str(datetime.datetime.now()) + ' ' +ctx.author.name)
    
    wait_msg = await ctx.send("Getting the co-codinates")
    start = 0
    while start < 5:
        await wait_msg.edit(content="LiveUpdate for 5 seconds")
        await wait_msg.edit(embed=iss_coordinates())
        start += 1
        time.sleep(1)
    
    await wait_msg.edit(embed=iss_coordinates(0))
# End of iss command ----------------------------------------------------------------------------------------

# Start of space search command -----------------------------------------------------------------------------

def space_search(search):
    response = requests.get("https://api.le-systeme-solaire.net/rest/bodies/{}".format(search))
    json_data = json.loads(response.text)
    embbed = discord.Embed(title='DATA',description='Some data maynot be accurate, API by `The Solar System OpenData`',color=0xCEB8FA)
    embbed.add_field(name='Name',value=json_data['name'],inline=False)
    embbed.add_field(name='English Name',value=json_data['englishName'],inline=False)
    embbed.add_field(name='Is Planet',value=json_data['isPlanet'],inline=False)
    embbed.add_field(name='Semi-major-Axis',value=str(json_data['semimajorAxis'])+ ' km',inline=False)
    embbed.add_field(name='Aphelion',value=str(json_data['aphelion'])+ ' km',inline=False)
    embbed.add_field(name='Gravity',value=str(json_data['gravity'])+ ' m/s^2',inline=False)
    embbed.add_field(name='Density',value=str(json_data['density'])+ ' g/cm^3',inline=False)
    embbed.add_field(name='Avg-Temp',value=str(json_data['avgTemp'])+ ' K',inline=False)
    return embbed
    



@client.command(brief='~ss [space body]',description='It will return some info about the space body you entered')
async def ss(ctx,search='earth'):
    wait_msg = await ctx.send("Getting the data for the space body, you entered")
    print('Space Search Command' + str(datetime.datetime.now()) + ' {} '.format(search) +ctx.author.name)
    try:
        await wait_msg.edit(content='Here you go...')
        await wait_msg.edit(embed=space_search(search))
    except:
        await wait_msg.edit(content='```Invalid Search Entry``` Make sure you spelled it right.')

@slash.slash(name='ss',description='space search for info about space bodies',options=[create_option(name='search',description='Enter the name of a space body, ex: Moon',option_type=3,required=True)])
async def ss(ctx,search='earth'):
    wait_msg = await ctx.send("Getting the data for the space body, you entered")
    print('Space Search Command' + str(datetime.datetime.now()) + '{} '.format(search) +ctx.author.name)
    try:
        await wait_msg.edit(content='Here you go...')
        await wait_msg.edit(embed=space_search(search))
    except:
        await wait_msg.edit(content='```Invalid Search Entry``` Make sure you spelled it right.')
# End os ss[Space search] command ----------------------------------------------------------------------------

@client.event
async def on_ready():
    print("I have logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Game(name=' ~help'))

    
# @client.event
# async def on_message(msg):
#     if msg.author == client.user:
#         return
#     if msg.content.startswith('-'):
#         await msg.channel.send('slash commands have been added, in order to use them, kick the current bot and re-invite it from the link https://reddysadala50.wixsite.com/curiosity')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('~'):
#         await message.channel.send("The new prefix for the bot is -")




client.run("YOUR BOT KEY")