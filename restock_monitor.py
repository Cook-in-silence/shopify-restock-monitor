import requests, json,time
from discord import Webhook, RequestsWebhookAdapter, Embed
import random
import threading


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

with open('C://Users//Administrator//Desktop//Cook in silence//shopify monitor//with quantity//links.txt', 'r') as f:
    product_urls = str(f.read()).split('\n')


def proxy_choice():
    with open('C://Users//Administrator//Desktop//Cook in silence//proxies.txt','r') as f:
        proxies = f.read().split('\n')
    proxy = random.choice(proxies)
    proxy_choice = {
        "http": "http://{}".format(proxy)
    }
    return proxy_choice


def icon_url():
    return 'https://cdn.discordapp.com/attachments/700177429850751096/725725896262156299/Silence_Notify.png'

def avatar_url():
    return 'https://cdn.discordapp.com/attachments/700177429850751096/725725896262156299/Silence_Notify.png'

def webhook_url():
    return '' # input your webhook url

def send_webhook(name,product_urls,description,product_price,product_image,new_status):
    url = webhook_url()
    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
    embed = Embed(title=name,url=''.join(product_urls),description=description)
    embed.add_field(name="price", value=product_price)
    embed.add_field(name="\u200b", value='\u200b')
    embed.add_field(name="\u200b", value='\u200b')
    embed.set_thumbnail(url=product_image)
    embed.add_field(name='sizes',value='\n'.join(list(new_status)))
    embed.set_footer(text='Cook in silence shopify monitor',icon_url=icon_url())
    webhook.send(embed=embed,avatar_url=avatar_url(),username='Cook in silence#8712')

def product_data(product_urls):
    new_status = []
    while True:
        for i in range(len(product_urls)):
            url_new = product_urls + ".json"
            domain_find = 'https://' + ''.join(product_urls).split('/')[2] + '/meta.json'
            response1 = requests.get(url_new, headers=headers,proxies=proxy_choice())
            response2 = requests.get(domain_find,headers=headers)
            j1 = json.loads(response1.text)
            j2 = json.loads(response2.text)
            product_title = j1["product"]['title']
            description = product_title
            product_image = j1['product']['images'][0]['src']
            product_variants = j1['product']['variants']
            product_price = j1['product']['variants'][0]['price']
            domain = j2['domain']
            name = j2['name']
            result = []
            for v in product_variants:
                title = v['title']
                id = v['id']
                atc_link = 'https://{}/cart/{}:1'.format(domain,id)
                inventory_quantity = v['inventory_quantity']
                v_result = "[{}]({}) ------ [ {} ]".format(title, atc_link, inventory_quantity)
                if inventory_quantity > 0:
                    result.append(v_result)
            last_status = result
            if len(last_status) == 0:
                time.sleep(0.01)
            else:
                try:
                    if len(new_status) == 0:
                        new_status = last_status
                        send_webhook(name,product_urls,description,product_price,product_image,new_status)
                    elif new_status != last_status:
                        new_status = last_status
                        send_webhook(name,product_urls,description,product_price,product_image,new_status)
                    elif new_status == last_status:
                        time.sleep(5)
                    else:
                        time.sleep(5)
                    time.sleep(1)
                except:
                    time.sleep(1)
            time.sleep(1)

if __name__ == "__main__":
    for i in product_urls:
        threading.Thread(name=str(i), target=product_data, args=(i,)).start()