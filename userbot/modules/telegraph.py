(C) 2019 The Raphielscape Company LLC.
#
# Licensed (
                    r_message,
                    TMP_DOWNLOAD_DIRECTORY
                )
                end = datetime.now()
                ms = (end - start).seconds
                await graph.edit("Downloaded to {} in {} seconds.".format(downloaded_file_name, ms))
                if downloaded_file_name.endswith((".webp")):
                    resize_image(downloaded_file_name)
                try:
                    start = datetime.now()
                    media_urls = upload_file(downloaded_file_name)
                except exceptions.TelegraphException as exc:
                    await graph.edit("ERROR: " + str(exc))
                    os.remove(downloaded_file_name)
                else:
                    end = datetime.now()
                    ms_two = (end - start).seconds
                    os.remove(downloaded_file_name)
                    await graph.edit("Uploaded to https://telegra.ph{} in {} seconds.".format(media_urls[0], (ms + ms_two)), link_preview=True)
            elif input_str == "text":
                user_object = await bot.get_entity(r_message.from_id)
                title_of_page = user_object.first_name # + " " + user_object.last_name
                # apparently, all Users do not have last_name field
                page_content = r_message.message
                if r_message.media:
                    if page_content != "":
                        title_of_page = page_content
                    downloaded_file_name = await bot.download_media(
                        r_message,
                        TMP_DOWNLOAD_DIRECTORY
                    )
                    m_list = None
                    with open(downloaded_file_name, "rb") as fd:
                        m_list = fd.readlines()
                    for m in m_list:
                        page_content += m.decode("UTF-8") + "\n"
                    os.remove(downloaded_file_name)
                page_content = page_content.replace("\n", "<br>")
                response = telegraph.create_page(
                    title_of_page,
                    html_content=page_content
                )
                end = datetime.now()
                ms = (end - start).seconds
                await graph.edit("Pasted to https://telegra.ph/{} in {} seconds.".format(response["path"], ms), link_preview=True)
        else:
            await graph.edit("Reply to a message to get a permanent telegra.ph link. (Inspired by @ControllerBot)")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


CMD_HELP.update({
    'telegraph': '.tg media | text\
        \nUsage: Upload text & media on Telegraph.\
        \nNotice: you are required to set TELEGRAPH_SHORT_NAME in Heroku vars for'

