def download_images(shortcode):
    '''
    Downloads Instagram Images to current directory

    Parameter(s):
        shortcode (str): shortcode of the instagram post
    '''

    import requests
    from datetime import datetime

    base_url = "https://www.instagram.com/p/"
    req_url = base_url + shortcode + "?__a=1"

    resp = requests.get(url=req_url).json()

    author = resp['graphql']['shortcode_media']['owner']['full_name']
    date = resp['graphql']['shortcode_media']['taken_at_timestamp']
    date = datetime.fromtimestamp(date).isoformat().replace('-','').replace(':','')+'Z'

    # if album of multiple images
    if 'edge_sidecar_to_children' in resp['graphql']['shortcode_media']:
        for i in resp['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
            image_url = i['node']['display_url']
            id_ = i['node']['id']

            filename = date+"_"+author+"_"+id_+".jpg"
            with requests.get(image_url, stream=True) as r:
                with open(filename, 'wb') as f:
                    f.write(r.content)
    else: # if only one image to the post
        image_url = resp['graphql']['shortcode_media']['display_url']
        id_ = resp['graphql']['shortcode_media']['id']

        filename = date+"_"+author+"_"+id_+".jpg"
        with requests.get(image_url, stream=True) as r:
            with open(filename, 'wb') as f:
                f.write(r.content)

def download_comments(shortcode):
    '''
    Downloads Instagram Comments to csv in current directory

    Parameter(s):
        shortcode (str): shortcode of the instagram post
    '''

    import requests
    from datetime import datetime

    base_url = "https://www.instagram.com"
    file_name = "/graphql/query/"
    url = base_url + file_name

    query_hash = "bc3296d1ce80a24b1b6e40b1e72903f5"
    first = 50
    variables = "{{\"shortcode\": \"{}\", \"first\":{}}}".format(shortcode, first)

    f = open("comments.csv",'w', encoding='utf-8')
    f.write("date, username, comment\n")
    has_next_page = True
    num_comments = 0
    while has_next_page:
        params = {
            'query_hash': query_hash,
            'variables': variables
            }
        resp = requests.get(url = url, params=params).json()

        total_count = resp['data']['shortcode_media']['edge_media_to_parent_comment']['count']

        has_next_page = resp['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
        after = resp['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']
        variables = """ {{"shortcode": "{}", "first":{}, "after": "{}" }}""".format(shortcode, first, after)

        # save comments to disk
        for comment in resp['data']['shortcode_media']['edge_media_to_parent_comment']['edges']:
            date = comment['node']['created_at']
            date = datetime.fromtimestamp(date).isoformat().replace('-','').replace(':','')+'Z'
            username = comment['node']['owner']['username']
            text = comment['node']['text'].replace("\n","\\n")

            f.write("{}, {}, {}\n".format(date, username, text))

            num_comments+=1
            print("\rComments Saved: {}/{}".format(num_comments, total_count), end="")
    f.close()

if __name__ == "__main__":
    import argparse
    import re

    parser = argparse.ArgumentParser(description="Downloads Instagram images/comments", epilog="Omit both optional arguments to download both")
    parser.add_argument('input_link', help="The link, or shortcode, of the post to download")
    parser.add_argument('-i', help="Download images only", action='store_true')
    parser.add_argument('-c', help="Download comments only", action='store_true')

    args=parser.parse_args()
    
    # extracts shortcode from url and (potential) suffix share bloat
    args.input_link = re.match(r'https://www.instagram.com/p/([-A-Za-z0-9]+)/?(.*)', args.input_link).group(1)
    if not args.c and not args.i:
        args.c = True
        args.i = True

    if args.i:
        download_images(args.input_link)
    
    if args.c:
        download_comments(args.input_link)
