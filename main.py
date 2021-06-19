from pyrogram import Client, filters, types
import os

sudolist = [1853611480]

API_ID = os.getenv('APIID')
API_HASH = os.getenv('APIHASH')
BOT_TOKEN = os.getenv('TOKEN')

app = Client('bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.regex(r'^/start'))
async def start(c: app, m: types.Message):
    texto = 'O HentaiWatchBot esta ativo.'
    texto += '\n\nQualquer duvida, olhe o /help.'
    await m.reply(texto)

@app.on_message(filters.regex(r'^/about'))
async def aboutbot(c: Client, m: types.Message):
    texto = 'Informações sobre o bot:'
    texto += '\nBot criado por [Luska1331](https://t.me/Luska1331)'
    texto += '\nRepo do bot: [HentaiWatchBot](https://github.com/Luska1331/HentaiWatchBot)'
    await m.reply(texto, parse_mode='md', disable_web_page_preview=True)


@app.on_message(filters.regex(r'^/changelog'))
async def changelog(c: app, m: types.Message):
    texto = '\n-> <code>/about</code> adicionado.'
    texto += '\n-> <code>/changelog</code> foi adicionado, uso global'
    texto += '\n-> <code>/getnhentai</code> foi adicionado como teste, uso somente no privado.'
    texto += '\n-> <code>/nhentai</code> foi adicionado como teste, uso global.' 
    await m.reply(texto, parse_mode='html')
    
@app.on_message(filters.regex('^/help'))
async def command_help(c: app, m: types.Message):
    texto = '\n<code>/getnhentai (ID)</code> -> Lhe envia as paginas do ID enviado.'
    texto += '\n<code>/nhentai (ID)</code> -> Lhe envia a capa juntamente com informaçoes basicas do ID definido.'
    texto += '\n<code>/nhentai</code> -> Lhe envia a capa juntamente com informaçoes basicas do hentai escolhido randomicamente.'
    texto += '\n<code>/changelog</code> -> Lhe envia uma lista com as ultimas mudanças no bot.'
    await m.reply(texto, parse_mode='html')

@app.on_message(filters.regex(r'^/shell (?P<text>.+)'))
async def shell(c: app, m: types.Message):
    import os
    if m.from_user.id in sudolist:
        code = m.matches[0]['text']
        import subprocess
        output = subprocess.getoutput(f'{code}')
        if len(output) > 4096:
            with open("output.txt", "w") as f:
                f.write(output)
            await m.reply_document("output.txt")
            return os.remove("output.txt")
        if output == '':
            await m.reply('command executed')
        else:
            await m.reply(output)

@app.on_message(filters.regex(r'^/echo (?P<text>.+)'))
async def echo(c: app,m: types.Message):
    arg = m.matches[0]['text']
    await m.reply(arg, parse_mode='md', disable_web_page_preview=True, disable_notification=True)

@app.on_message(filters.regex(r'^/nhentai (?P<text>.+)'))
async def pornhub(c: app, m: types.Message):
    mensagem = m.matches[0]['text']
    if mensagem:
        if mensagem.isdecimal():
            try:
                from hentai import Hentai, Format, Utils
                nid = mensagem
                doujin = Hentai(nid)
                texto = f'Data de Upload: <code>{doujin.upload_date}</code>'
                texto += f'Titulo: {doujin.title()}'
                texto += f'\nID: <code>{nid}</code>'
                texto += f'\nTags: '
                for tag in doujin.tag:
                    texto +=  f'{tag.name} | '
                texto += f'\nLink: {doujin.url}'
                photo = doujin.cover
                await m.reply_photo(photo, caption=texto, parse_mode='HTML')
                texto += f'\nPedido do(a) {m.from_user.mention}'
                await c.send_photo(chat_id='-1001166306279', photo=photo, caption=texto, parse_mode='html')
            except:
                await m.reply('ID invalido, tente novamente, seu corno.')
        else:
            await m.reply('Digita um numero, seu animal.')

@app.on_message(filters.regex('^/nhentai'))
async def nhentai(c: app, m: types.Message):
    from hentai import Hentai, Format, Utils
    nid = Utils.get_random_id()
    doujin = Hentai(nid)
    texto = f'Data de Upload: <code>{doujin.upload_date}</code>'
    texto += f'Titulo: {doujin.title()}'
    texto += f'\nID: <code>{nid}</code>'
    texto += f'\nTags: '
    for tag in doujin.tag:
        texto +=  f'{tag.name} | '
    texto += f'\nLink: {doujin.url}'
    photo = doujin.cover
    await m.reply_photo(photo, caption=texto, parse_mode='HTML')
    texto += f'\nPedido do(a) {m.from_user.mention}'
    await c.send_photo(chat_id='-1001166306279', photo=photo, caption=texto)

@app.on_message(filters.regex(r'^/getnhentai (?P<text>.+)'))
async def getnhentai(c: app, m: types.Message):
    nhentai = m.matches[0]['text']
    from hentai import Hentai, Format
    if m.chat.id == m.from_user.id:
        if nhentai.isdecimal():
            try:
                doujin = Hentai(nhentai)
                if len(doujin.image_urls) > 30:
                    await m.reply('Por questoes de segurança, estou limitado a somente 30 paginas.')
                else:
                    for i in doujin.image_urls:
                        await m.reply_photo(i, disable_notification=True)
                    await m.reply('FIM')
            except:
                await m.reply('ID invalido')
        else:
            await m.reply('Digita numeros, imbecil')
    else:
        await m.reply('Uso somente no privado')
        

app.run()
